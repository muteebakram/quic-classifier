import os

DATASET_NAME = "final-dataset.csv"

os.remove(DATASET_NAME)
write = open(DATASET_NAME, "a")
files = [
    "CSV/dataset2.csv",
    "CSV/dataset3.csv",
    "CSV/dataset4.csv",
    "CSV/dataset5.csv",
    "CSV/google_hangouts.csv",
    "CSV/youtube.csv",
]


def write_csv(input_file):
    read = open(input_file, "r")
    # Skip the headers
    # next(read)
    for line in read:
        if "frame.encap_type,frame.time_epoch,frame.len,frame.cap_len" in line:
            print("skipped")
            continue
        write.write(line)
    read.close()


# Add the headers
write.write(
    "frame.encap_type,frame.time_epoch,frame.len,frame.cap_len,eth.src,eth.dst,ip.version,ip.hdr_len,ip.tos,ip.id,ip.flags,ip.flags.rb,ip.flags.df,ip.flags.mf,ip.frag_offset,ip.ttl,ip.proto,ip.checksum,ip.src,ip.dst,ip.len,ip.dsfield,tcp.srcport,tcp.dstport,tcp.hdr_len,tcp.checksum,udp.srcport,udp.dstport,udp.length,udp.checksum,quic\n"
)

for file in files:
    write_csv(file)
    print("Added file: ", file)

write.close()
