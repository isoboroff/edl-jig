import argparse

from manager import Manager


def str_to_bool(s):
    s = s.lower()
    if s == "true":
        return True
    elif s == "false":
        return False
    else:
        raise argparse.ArgumentTypeError("Expected boolean value.")


if __name__ == "__main__":
    manager = Manager()

    parser = argparse.ArgumentParser()
    parser_sub = parser.add_subparsers()

    # Specific to prepare
    parser_prepare = parser_sub.add_parser("prepare")
    parser_prepare.set_defaults(run=manager.prepare)
    parser_prepare.add_argument("--repo", required=True, type=str, help="the image repo (i.e., osirrc2019/anserini)")
    parser_prepare.add_argument("--tag", default="latest", type=str, help="the image tag (i.e., latest)")
    parser_prepare.add_argument("--save_to_snapshot", default="save", type=str, help="used to determine the tag of the snapshotted image after indexing")
    parser_prepare.add_argument("--collections", nargs="+", help="the name of the collection")
    parser_prepare.add_argument("--opts", nargs="+", default="", type=str, help="the args passed to the index script")

    # Specific to train
    trainer_prepare = parser_sub.add_parser("train")
    trainer_prepare.set_defaults(run=manager.train)
    trainer_prepare.add_argument("--repo", required=True, type=str, help="the image repo (i.e., albep/nvsm)")
    trainer_prepare.add_argument("--tag", default="latest", type=str, help="the image tag (i.e., latest)")
    trainer_prepare.add_argument("--load_from_snapshot", default="save", type=str, help="used to determine the tag of the snapshotted image to train from")
    trainer_prepare.add_argument("--collection", help="the name of the collection for train")
    trainer_prepare.add_argument("--save_to_snapshot", default="save", type=str, help="used to determine the tag of the snapshotted image after indexing")
    trainer_prepare.add_argument("--train_split", required=True, type=str, help="the subset of topic ids to use for training")
    trainer_prepare.add_argument("--validation_split", required=True, type=str, help="the subset of topic ids to use for validation")
    trainer_prepare.add_argument("--model_folder", required=True, type=str, help="folder where to store the trained model")
    trainer_prepare.add_argument("--gold", required=True, type=str, help="the annotations file for model selection")
    trainer_prepare.add_argument("--opts", nargs="+", default="", type=str, help="the args passed to the index script")
    trainer_prepare.add_argument("--version", default="", type=str, help="the version string passed to the init script")
    trainer_prepare.add_argument("--gpu", default=False, type=bool, help="Boolean to enable the use of the gpu on supported docker images (i.e., albep/nvsm_gpu)")


    # Specific to test
    parser_test = parser_sub.add_parser("test")
    parser_test.set_defaults(run=manager.tester)
    parser_test.add_argument("--repo", required=True, type=str, help="the image repo (i.e., osirrc2019/anserini)")
    parser_test.add_argument("--tag", default="latest", type=str, help="the image tag (i.e., latest)")
    parser_test.add_argument("--load_from_snapshot", default="save", type=str, help="used to determine the tag of the snapshotted image to search from")
    parser_test.add_argument("--collection", required=True, help="the name of the collection")
    parser_test.add_argument("--output", required=True, type=str, help="the output directory for run files on the host")
    parser_test.add_argument("--gold", required=True, type=str, help="the annotations file for evaluation")
    parser_test.add_argument("--test_split", required=False, default="", type=str, help="the subset of topic ids to use for testing")
    parser_test.add_argument("--opts", nargs="+", default="", type=str, help="the args passed to the search script")
    parser_test.add_argument("--timings", action="store_true", help="enable timing information to be printed")
    parser_test.add_argument("--gpu", default=False, type=bool, help="Boolean to enable the use of the gpu on supported docker images (i.e., albep/nvsm_gpu)")
    parser_test.add_argument("--measures", nargs="+", default=["num_q", "map", "P.30", "ndcg_cut.20"], type=str, help="the measures for trec_eval")

    # Specific to interact
    parser_interact = parser_sub.add_parser("interact")
    parser_interact.set_defaults(run=manager.interact)
    parser_interact.add_argument("--repo", required=True, type=str, help="the image repo (i.e., osirrc2019/anserini)")
    parser_interact.add_argument("--tag", default="latest", type=str, help="the image tag (i.e., latest)")
    parser_interact.add_argument("--load_from_snapshot", default="save", type=str, help="used to determine the tag of the snapshotted image to interact with")
    parser_interact.add_argument("--exit_jig", default="false", type=str_to_bool, help="whether to exit jig after running container")
    parser_interact.add_argument("--opts", nargs="+", default="", type=str, help="the args passed to the interact script")

    # Parse the args
    args = parser.parse_args()
    args.run(args)
