from initialize_config import initialize_config, dataset_loader

import json
import argparse
import time
import datetime
import os
import sys

from open3d_example import *

# pyexample_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(pyexample_path)
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# get absolute path of this file

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = (
    os.path.abspath(os.path.join(dir_path, os.pardir)) + "/config/synthetic_data.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconstruction system")
    parser.add_argument(
        "--make", help="Step 1) make fragments from RGBD sequence.", action="store_true"
    )
    # parser.add_argument(
    #    "--register",
    #    help="Step 2) register all fragments to detect loop closure.",
    #    action="store_true",
    # )
    # parser.add_argument(
    #    "--refine", help="Step 3) refine rough registrations", action="store_true"
    # )
    # parser.add_argument(
    #    "--integrate",
    #    help="Step 4) integrate the whole RGBD sequence to make final mesh.",
    #    action="store_true",
    # )
    # parser.add_argument(
    #    "--slac",
    #    help="Step 5) (optional) run slac optimization for fragments.",
    #    action="store_true",
    # )
    # parser.add_argument(
    #    "--slac_integrate",
    #    help="Step 6) (optional) integrate fragments using slac to make final "
    #    "pointcloud / mesh.",
    #    action="store_true",
    # )
    parser.add_argument("--debug_mode", help="turn on debug mode.", action="store_true")

    args = parser.parse_args()

    if (
        not args.make
        and not args.register
        and not args.refine
        and not args.integrate
        and not args.slac
        and not args.slac_integrate
    ):
        parser.print_help(sys.stderr)
        sys.exit(1)

    # load dataset and check folder structure
    with open(config_path) as json_file:
        config = json.load(json_file)
        initialize_config(config)
        check_folder_structure(config['path_dataset'])

    assert config is not None

    if args.debug_mode:
        config["debug_mode"] = True
    else:
        config["debug_mode"] = False

    config["device"] = "cpu:0"

    print("====================================")
    print("Configuration")
    print("====================================")
    for key, val in config.items():
        print("%40s : %s" % (key, str(val)))

    times = [0, 0, 0, 0, 0, 0]
    if args.make:
        start_time = time.time()
        import make_fragments

        make_fragments.run(config)
        times[0] = time.time() - start_time
    # if args.register:
    #    start_time = time.time()
    #    import register_fragments

    #    register_fragments.run(config)
    #    times[1] = time.time() - start_time
    # if args.refine:
    #    start_time = time.time()
    #    import refine_registration

    #    refine_registration.run(config)
    #    times[2] = time.time() - start_time
    # if args.integrate:
    #    start_time = time.time()
    #    import integrate_scene

    #    integrate_scene.run(config)
    #    times[3] = time.time() - start_time
    # if args.slac:
    #    start_time = time.time()
    #    import slac

    #    slac.run(config)
    #    times[4] = time.time() - start_time
    # if args.slac_integrate:
    #    start_time = time.time()
    #    import slac_integrate

    #    slac_integrate.run(config)
    #    times[5] = time.time() - start_time

    print("====================================")
    print("Elapsed time (in h:m:s)")
    print("====================================")
    print("- Making fragments    %s" % datetime.timedelta(seconds=times[0]))
    print("- Register fragments  %s" % datetime.timedelta(seconds=times[1]))
    print("- Refine registration %s" % datetime.timedelta(seconds=times[2]))
    print("- Integrate frames    %s" % datetime.timedelta(seconds=times[3]))
    print("- SLAC                %s" % datetime.timedelta(seconds=times[4]))
    print("- SLAC Integrate      %s" % datetime.timedelta(seconds=times[5]))
    print("- Total               %s" % datetime.timedelta(seconds=sum(times)))
    sys.stdout.flush()
