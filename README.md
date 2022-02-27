# Quic Classifier of QUIC and Non-QUIC packets

## 1. Capture packets

Download and install wireshark and capture packets and save as pcap file.

or

Capture packets using `tcpdump`

```sh
tcpdump -s 0 -i <interface-name> -w <file-name.pcap>
```

Example:

```sh
tcpdump -s 0 -i en0 -w initial-capture.pcap
```

[tcpdump to pcap](https://linuxexplore.com/2012/06/07/use-tcpdump-to-capture-in-a-pcap-file-wireshark-dump/)

## 2. Convert pcap files to CSV.

There are many ways to convert pcap to csv. But we need only specific feilds and this is easiest way. Command to generate CSV from pcap file.

```sh
tshark -r initial-capture.pcap  -T fields -E header=y -E separator=, -E occurrence=f  -e frame.encap_type -e frame.time_epoch -e frame.len -e frame.cap_len -e eth.src -e eth.dst -e ip.version -e ip.hdr_len -e ip.tos -e ip.id -e ip.flags -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e ip.checksum -e ip.src -e ip.dst -e ip.len -e ip.dsfield -e tcp.srcport -e tcp.dstport -e tcp.hdr_len -e tcp.checksum -e udp.srcport -e udp.dstport -e udp.length -e udp.checksum -e quic > initial.csv
```

tshark -r initial-capture.pcap -T fields -E header=y -E separator=, -E occurrence=f -e frame.encap_type -e frame.time_epoch -e frame.len -e frame.cap_len -e eth.src -e eth.dst -e ip.version -e ip.hdr_len -e ip.tos -e ip.id -e ip.flags -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e ip.checksum -e ip.src -e ip.dst -e ip.len -e ip.dsfield -e tcp.srcport -e tcp.dstport -e tcp.hdr_len -e tcp.checksum -e udp.srcport -e udp.dstport -e udp.length -e udp.checksum -e quic > data.csv

## [TODO] Collect all the csv and shuffle the rows.

## 4. Merge the respective columns from tcp & udp.

As we know QUIC uses UDP protocol. Therefore, we have taken common feilds from TCP and UDP protocol ie, srcport,dstport,length,checksum. Run the below command to merge the columns and rename the column names.

**Before:** tcp.srcport,tcp.dstport,tcp.hdr_len,tcp.checksum,udp.srcport,udp.dstport,udp.length,udp.checksum

**After :** srcport,dstport,length,checksum

```
python3 merge_columns.py
```

## 5. Run the ML Models

- Run all the cells from `quic-classifier.ipynb`

- Directly see the results by opening HTML file `quic-classifier.html`
