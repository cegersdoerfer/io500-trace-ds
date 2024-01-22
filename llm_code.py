
import pandas as pd

# Re-defining the function to parse the Darshan log file
def parse_darshan_txt(txt_output):
    # Lists to store extracted data
    file_ids = []
    apis = []
    ranks = []
    operations = []
    segments = []
    offsets = []
    sizes = []
    starts = []
    ends = []
    osts = []
    # Variables to hold temporary data
    current_file_id = None
    current_rank = None
    current_api = 'POSIX'
    trace_start_time = None
    full_runtime = None
    
    for line in txt_output.splitlines():
        # Extract start time
        if line.startswith("# start_time:"):
            trace_start_time = float(line.split(':')[1].strip())
        
        if line.startswith("# run time:"):
            full_runtime = float(line.split(':')[1].strip())

        # Extract file_id
        if line.startswith("# DXT, file_id:"):
            current_file_id = line.split(':')[1].split(',')[0].strip()
            
        # Extract rank
        if line.startswith("# DXT, rank:"):
            current_rank = line.split(':')[1].split(',')[0].strip()
            
        # Extract IO operation details
        if not line.startswith("#") and current_file_id and current_rank:
            parts = line.split()
            # Check if the line has the expected number of fields
            if len(parts) < 8:
                continue
            operations.append(parts[2])
            ranks.append(current_rank)
            file_ids.append(current_file_id)
            apis.append(current_api)
            segments.append(int(parts[3]))
            if parts[4] == 'N/A':
                offsets.append(0)
            else:
                offsets.append(int(parts[4]))
            if parts[5] == 'N/A':
                sizes.append(0)
            else:
                sizes.append(int(parts[5]) / 1000000)  # Convert to MB
            starts.append(float(parts[6]) + trace_start_time)
            ends.append(float(parts[7]) + trace_start_time)
            if len(parts) >= 9:
                ost_info = ','.join(parts[9:]).replace(']', '')
                osts.append(ost_info)
            else:
                osts.append('')
                
    # Create DataFrame
    df = pd.DataFrame({
        'file_id': file_ids,
        'api': apis,
        'rank': ranks,
        'operation': operations,
        'segment': segments,
        'offset': offsets,
        'size': sizes,
        'start': starts,
        'end': ends,
        'ost': osts
    })
    df = pd.DataFrame.from_dict(df).sort_values(by=['start'])
    df.reset_index(drop=True, inplace=True)
    
    return df, trace_start_time, full_runtime

# Load the uploaded log file
file_path = 'labelled-issues/random-access/ior-rnd1MB_api_MPIIO_blockSize_1073741824_randomPrefill_0_.txt'
with open(file_path, 'r') as file:
    log_content = file.read()

# Parse the log file
df, trace_start_time, full_runtime = parse_darshan_txt(log_content)
df.head()  # Displaying the first few rows of the parsed data


# Function to detect large numbers of small reads/writes
def detect_small_io(df, threshold_size_mb=1, threshold_percentage=10):
    small_io = df[df['size'] < threshold_size_mb]
    total_io = df.shape[0]
    small_read_percentage = (small_io[small_io['operation'] == 'read'].shape[0] / total_io) * 100
    small_write_percentage = (small_io[small_io['operation'] == 'write'].shape[0] / total_io) * 100

    small_io_issues = {
        'small_read_issue': small_read_percentage > threshold_percentage,
        'small_write_issue': small_write_percentage > threshold_percentage
    }
    return small_io_issues

# Function to detect re-reads or full-size reads
def detect_reread_fullsize_reads(df):
    file_sizes = {}  # Dictionary to store total read size per file
    re_read_issues = {}
    for file_id in df['file_id'].unique():
        file_data = df[df['file_id'] == file_id]
        total_read_size = file_data[file_data['operation'] == 'read']['size'].sum()
        # Placeholder for actual file size (needs to be obtained from the application or filesystem)
        actual_file_size = 100  # This is a placeholder value
        re_read_issues[file_id] = total_read_size > actual_file_size

    return re_read_issues

def detect_inefficient_reads(df):
    inefficient_read_issues = {}
    for file_id in df['file_id'].unique():
        file_data = df[df['file_id'] == file_id]
        # Determine the maximum write offset for the file
        max_write_offset = file_data[file_data['operation'] == 'write']['offset'].max()

        # Analyze read operations
        read_operations = file_data[file_data['operation'] == 'read']
        read_beyond_write = any((read_operations['offset'] + read_operations['size']) > max_write_offset)
        repeated_reads = read_operations.duplicated(subset=['offset', 'size'], keep=False).any()

        inefficient_read_issues[file_id] = read_beyond_write or repeated_reads

    return inefficient_read_issues


# Additional analysis functions

# Function to detect stripe misalignment
def detect_stripe_misalignment(df, stripe_size_mb):
    misalignment_issues = {}
    for file_id in df['file_id'].unique():
        file_data = df[df['file_id'] == file_id]
        misaligned_operations = file_data[(file_data['size'] % stripe_size_mb) != 0]
        misalignment_issues[file_id] = misaligned_operations.shape[0] > 0
    return misalignment_issues

# Function to analyze spatiality of requests
def analyze_spatiality(df):
    spatiality_issues = {}
    for file_id in df['file_id'].unique():
        file_data = df[df['file_id'] == file_id]
        # Placeholder for spatiality analysis logic
        # For now, just setting a placeholder value
        spatiality_issues[file_id] = "random"  # Placeholder
    return spatiality_issues

# Function to check balance of I/O requests across ranks
def check_io_balance(df, balance_threshold=15):
    balance_issues = {}
    for file_id in df['file_id'].unique():
        file_data = df[df['file_id'] == file_id]
        rank_io_counts = file_data['rank'].value_counts()
        max_io = rank_io_counts.max()
        min_io = rank_io_counts.min()
        imbalance_percentage = ((max_io - min_io) / max_io) * 100
        balance_issues[file_id] = imbalance_percentage > balance_threshold
    return balance_issues

# Function to evaluate time spent in metadata operations
def evaluate_metadata_time(df, time_threshold=30):
    metadata_issues = {}
    for rank in df['rank'].unique():
        rank_data = df[df['rank'] == rank]
        metadata_time = rank_data[rank_data['operation'].isin(['open', 'close', 'stat', 'seek'])]['size'].sum()
        metadata_issues[rank] = metadata_time > time_threshold
    return metadata_issues

# Function to analyze STDIO usage
def analyze_stdio_usage(df, stdio_threshold=10):
    stdio_issues = {}
    total_transfer_size = df['size'].sum()
    stdio_transfer_size = df[df['api'] == 'STDIO']['size'].sum()
    stdio_percentage = (stdio_transfer_size / total_transfer_size) * 100
    stdio_issues['excessive_stdio_usage'] = stdio_percentage > stdio_threshold
    return stdio_issues

# Testing the new functions
stripe_size_mb = 1  # Placeholder for stripe size, should be set according to the file system
stripe_misalignment_issues = detect_stripe_misalignment(df, stripe_size_mb)
spatiality_issues = analyze_spatiality(df)
io_balance_issues = check_io_balance(df)
metadata_time_issues = evaluate_metadata_time(df)
stdio_usage_issues = analyze_stdio_usage(df)
small_io_issues = detect_small_io(df)
re_read_issues = detect_inefficient_reads(df)

# Displaying the results
print("Stripe misalignment issues:")
print(stripe_misalignment_issues)
print("Spatiality issues:")
print(spatiality_issues)
print("I/O balance issues:")
print(io_balance_issues)
print("Metadata time issues:")
print(metadata_time_issues)
print("STDIO usage issues:")
print(stdio_usage_issues)
print("Small I/O issues:")
print(small_io_issues)
print("Re-read issues:")
print(re_read_issues)



