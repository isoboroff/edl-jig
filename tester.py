import json
import os
import re
import subprocess
import sys


class Tester:

    def __init__(self, tester_config=None):
        self.config = tester_config

    def set_config(self, tester_config):
        self.config = tester_config

    def test(self, client, output_path_guest, test_split_path_guest, generate_save_tag):
        """
        Runs the detector and evaluates the results (run files placed into the /output directory) using neleval
        """
        save_tag = generate_save_tag(self.config.tag, self.config.load_from_snapshot)

        exists = len(client.images.list(filters={"reference": "{}:{}".format(self.config.repo, save_tag)})) != 0
        if not exists:
            sys.exit("Must prepare image first...")

        output_path = os.path.abspath(self.config.output)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        volumes = {
            output_path: {
                "bind": output_path_guest,
                "mode": "rw"
            },
        }

        if len(self.config.test_split) > 0:
            volumes[os.path.abspath(self.config.test_split)] = {"bind": test_split_path_guest, "mode": "ro"}

        test_args = {
            "collection": {
                "name": self.config.collection
            },
            "opts": {key: value for (key, value) in map(lambda x: x.split("="), self.config.opts)},
            "test_split": {
                "path": test_split_path_guest
            },
        }

        # The test command
        command = "sh -c '/test --json {}'"
        runtime = "nvidia" if self.config.gpu else "runc"

        if self.config.timings:
            # The search command with timings
            command = "sh -c 'time -p /test --json {}'"

        # Time the EDL run
        print("Starting container from saved image...")

        container = client.containers.run("{}:{}".format(self.config.repo, save_tag), command.format(json.dumps(json.dumps(test_args))), volumes=volumes,
                                          detach=True, runtime=runtime)

        test_times = []
        print("Logs for search in container with ID {}...".format(container.id))
        for line in container.logs(stream=True):
            if self.config.timings:
                match = re.match('^(real|user|sys)\\s(.*)$', line.decode('utf-8'))
                if match:
                    test_times.append(match)
            print(str(line.decode('utf-8')), end="")

        if self.config.timings:
            print()
            print('**********')
            print('Detection timing information')
            print(test_times[0].group(0))
            print(test_times[1].group(0))
            print(test_times[2].group(0))
            print()

        # The measure string passed to neleval
        ### TODO this needs to be updated for NEL
        measures = " ".join(map(lambda x: "-c -m {}".format(x), self.config.measures))

        print("Evaluating results using neleval...")
        for file in os.listdir(self.config.output):
            if not file.endswith("neleval"):
                run = os.path.join(self.config.output, file)
                print("###\n# {}\n###".format(run))
                try:
                    result = subprocess.check_output("neleval/nel {} {} {}".format(measures, self.config.qrels, run).split())
                    print(result.decode("UTF-8"))
                    with open("{}.trec_eval".format(run), "w+") as out:
                        out.write(result.decode("UTF-8"))
                except subprocess.CalledProcessError:
                    print("Unable to evaluate {} - is it a run file?".format(run))
