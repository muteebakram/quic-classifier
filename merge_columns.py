# Goal merge the columns
# Before: tcp.srcport,tcp.dstport,tcp.hdr_len,tcp.checksum,udp.srcport,udp.dstport,udp.length,udp.checksum
# After : srcport,dstport,length,checksum

import csv
import argparse


quic_counter = 0
total_packets = 0

parser = argparse.ArgumentParser(
    description="Mege the common columns ie srcport,dstport,length,checksum"
)
parser.add_argument(
    "-i", "--input-file", help="Input csv file of pcap file.", required=False
)
parser.add_argument(
    "-o", "--output-file", help="Merged columns output file.", required=False
)
args = vars(parser.parse_args())

if args["input_file"]:
    INPUT_FILE = args["input_file"]
else:
    INPUT_FILE = "dataset5.csv"

if args["output_file"]:
    OUTPUT_FILE = args["output_file"]
else:
    OUTPUT_FILE = "output-dataset.csv"


with open(INPUT_FILE) as f, open(OUTPUT_FILE, "w") as g:
    reader = csv.reader(f)
    writer = csv.writer(g)

    headers = next(reader, None)  # skip the headers
    # writer.writerow(headers[:-4])
    writer.writerow(
        [
            "frame.encap_type",
            "frame.time_epoch",
            "frame.len",
            "frame.cap_len",
            "eth.src",
            "eth.dst",
            "ip.version",
            "ip.hdr_len",
            "ip.tos",
            "ip.id",
            "ip.flags",
            "ip.flags.rb",
            "ip.flags.df",
            "ip.flags.mf",
            "ip.frag_offset",
            "ip.ttl",
            "ip.proto",
            "ip.checksum",
            "ip.src",
            "ip.dst",
            "ip.len",
            "ip.dsfield",
            "srcport",
            "dstport",
            "length",
            "checksum",
            "quic",
        ]
    )
    for row in reader:
        # print("Merging srcport...")
        if not row[22] and not row[26]:
            srcport = ""
        elif row[22]:
            srcport = row[22]
        elif row[26]:
            srcport = row[26]
        else:
            srcport = ""

        if not srcport:
            print("Empty srcport, skipping row: ", row)
            continue

        # print("Merging dstport...")
        if not row[23] and not row[27]:
            dstport = ""
        elif row[23]:
            dstport = row[23]
        elif row[27]:
            dstport = row[27]
        else:
            dstport = ""

        if not dstport:
            print("Empty dstport, skipping row: ", row)
            continue

        # print("Merging length...")
        if not row[24] and not row[28]:
            length = ""
        elif row[24]:
            length = row[24]
        elif row[28]:
            length = row[28]
        else:
            length = ""

        if not length:
            print("Empty length, skipping row: ", row)
            continue

        # print("Merging checksum...")
        if not row[25] and not row[29]:
            checksum = ""
        elif row[25]:
            checksum = row[25]
        elif row[29]:
            checksum = row[29]
        else:
            checksum = ""

        if not checksum:
            print("Empty checksum, skipping row: ", row)
            continue

        # print(row[-1])
        if row[-1]:
            quic = 1
            quic_counter += 1
        else:
            quic = 0

        new_row = row[:22] + [srcport] + [dstport] + [length] + [checksum] + [quic]
        # print(new_row)

        total_packets += 1
        writer.writerow(new_row)

print(
    "\nQuic packets: {0}, Non-Quic packets: {1}, Total: {2}, Percentage: {3}%".format(
        quic_counter,
        total_packets - quic_counter,
        total_packets,
        round((quic_counter / total_packets) * 100, 2),
    )
)
