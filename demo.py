import os
import joblib
import pandas as pd

PCAP_FILE_PATH = "example.pcap"
OUTPUT_FILE_PATH = "initial-dataset.csv"
DATASET_FILE_PATH = "merged-dataset.csv"


def preprocess(ds):

    # 1. Remove the strings columnns from dataset.
    # eth.src, eth.dst, ip.src, ip.dst, ip.tos, ip.id, ip.flags, ip.checksum, ip.dsfield, checksum
    ds.drop(
        [
            "eth.src",
            "eth.dst",
            "ip.src",
            "ip.dst",
            "ip.tos",
            "ip.id",
            "ip.flags",
            "ip.checksum",
            "ip.dsfield",
            "checksum",
        ],
        axis=1,
        inplace=True,
    )

    # 2. Remove the invalid rows ie axis=0 from the dataset.
    ds.dropna(axis=0, inplace=True)

    # 3. After deleting the rows, reset the index column and delete it.
    ds.reset_index(drop=True)

    # 4. Get the result(quic) column values and remove dataset.
    targets = list(ds["quic"].values)
    ds.drop(ds.columns[len(ds.columns) - 1], axis=1, inplace=True)

    # print(ds.info())
    return ds, targets


def is_quic(packet):
    if packet:
        return "quic"
    else:
        return "non-quic"


if __name__ == "__main__":

    pcap_to_csv_cmd = "tshark -r '{0}' -T fields -E header=y -E separator=, -E occurrence=f  -e frame.encap_type \
            -e frame.time_epoch -e frame.len -e frame.cap_len -e eth.src -e eth.dst -e ip.version \
            -e ip.hdr_len -e ip.tos -e ip.id -e ip.flags -e ip.flags.rb -e ip.flags.df -e ip.flags.mf \
            -e ip.frag_offset -e ip.ttl -e ip.proto -e ip.checksum -e ip.src -e ip.dst -e ip.len \
            -e ip.dsfield -e tcp.srcport -e tcp.dstport -e tcp.hdr_len -e tcp.checksum -e udp.srcport \
            -e udp.dstport -e udp.length -e udp.checksum -e quic > '{1}'".format(
        PCAP_FILE_PATH, OUTPUT_FILE_PATH
    )
    # print(pcap_to_csv_cmd)

    os.system(pcap_to_csv_cmd)
    print("Generated CSV file from {0}...\n".format(PCAP_FILE_PATH))

    os.system(
        "python merge_columns.py -i {0} -o {1} > /dev/null".format(
            OUTPUT_FILE_PATH, DATASET_FILE_PATH
        )
    )
    print("Merged common columns in dataset...\n")

    dataset = pd.read_csv(DATASET_FILE_PATH)
    X_test, Y_test = preprocess(dataset)
    print("Dataset preprocess completed...\n")

    logistic_regression_path = os.path.join("models", "LogisticRegression")
    naive_bayes_path = os.path.join("models", "NaiveBayes")
    gradient_boosting_classifier_path = os.path.join(
        "models", "GradientBoostingClassifier"
    )
    decision_tree_classifier_path = os.path.join("models", "DecisionTreeClassifier")
    k_neighbors_classifier_path = os.path.join("models", "KNeighborsClassifier")
    random_forest_classifier_path = os.path.join("models", "RandomForestClassifier")

    logistic_regression_model = joblib.load(logistic_regression_path)
    naive_bayes_model = joblib.load(naive_bayes_path)
    gradient_boosting_classifier_model = joblib.load(gradient_boosting_classifier_path)
    decision_tree_classifier_model = joblib.load(decision_tree_classifier_path)
    k_neighbors_classifier_model = joblib.load(k_neighbors_classifier_path)
    random_forest_classifier_model = joblib.load(random_forest_classifier_path)

    print("Acuracy...\n")
    print(
        "{0:<35} {1}%".format(
            "Logistic_Regression_Model",
            round(logistic_regression_model.score(X_test, Y_test) * 100, 2),
        )
    )
    print(
        "{0:<35} {1}%".format(
            "Naive_Bayes",
            round(naive_bayes_model.score(X_test, Y_test) * 100, 2),
        )
    )
    print(
        "{0:<35} {1}%".format(
            "Gradient_Boosting_Classifier_Model",
            round(gradient_boosting_classifier_model.score(X_test, Y_test) * 100, 2),
        )
    )
    print(
        "{0:<35} {1}%".format(
            "Decision_Tree_Classifier_Model",
            round(decision_tree_classifier_model.score(X_test, Y_test) * 100, 2),
        )
    )

    print(
        "{0:<35} {1}%".format(
            "K_Neighbors_Classifier_Model",
            round(k_neighbors_classifier_model.score(X_test, Y_test) * 100, 2),
        )
    )

    print(
        "{0:<35} {1}%".format(
            "Random_Forest_Classifier_Model",
            round(random_forest_classifier_model.score(X_test, Y_test) * 100, 2),
        )
    )

    print("\nPrediction...\n")
    logistic_regression_prediction = logistic_regression_model.predict(X_test)
    naive_bayes_prediction = naive_bayes_model.predict(X_test)
    gradient_boosting_classifier_prediction = gradient_boosting_classifier_model.predict(
        X_test
    )
    decision_tree_classifier_prediction = decision_tree_classifier_model.predict(X_test)
    k_neighbors_classifier_prediction = k_neighbors_classifier_model.predict(X_test)
    random_forest_classifier_prediction = random_forest_classifier_model.predict(X_test)

    print(
        "{0:<28} {1:<28} {2:<28} {3:<28} {4:<28} {5:<28} {6:<28} {7:<28}".format(
            "Packet Time",
            "Logistic_Regression",
            "Naive_Bayes",
            "Gradient_Boosting_Classifier",
            "Decision_Tree_Classifier",
            "K_Neighbors_Classifier",
            "Random_Forest_Classifier",
            "Actual Packet Protocol",
        )
    )

    for index, test in enumerate(X_test.values):
        print(
            "{0:<28} {1:<28} {2:<28} {3:<28} {4:<28} {5:<28} {6:<28} {7:<28}".format(
                "{0}-{1}".format(index, test[1]),
                is_quic(logistic_regression_prediction[index]),
                is_quic(naive_bayes_prediction[index]),
                is_quic(gradient_boosting_classifier_prediction[index]),
                is_quic(decision_tree_classifier_prediction[index]),
                is_quic(k_neighbors_classifier_prediction[index]),
                is_quic(random_forest_classifier_prediction[index]),
                is_quic(Y_test[index]),
            )
        )
