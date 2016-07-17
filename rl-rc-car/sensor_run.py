"""
Used to launch sensor readers. We need this because different sensors
return readings at different speeds, so we launch multiple processes
to run semi-concurrently.
"""
import argparse
import redis
import sys
import json

r_server = redis.Redis('localhost')
verbose = True


def do_sonar(pins):
    from sensors.sensors import SonarSensor
    sonar = SonarSensor(pins[1], pins[0])

    while True:
        sonar_reading = sonar.get_reading()
        r_server.set('s_m', int(sonar_reading))

        if verbose:
            print(sonar_reading)


def do_ir_sweep(arduino_path):
    from sensors.sensors import IRSweep
    try:
        ir_sweep = IRSweep(path=arduino_path)
    except:
        print("Couldn't find an Arduino at %s" % arduino_path)
        print("Exiting.")
        sys.exit(0)

    while True:
        print("Sweeping.")
        new_sweeps = ir_sweep.get_ir_sweep_reading()
        new_sweeps_str = json.dumps(new_sweeps)

        # Write them...
        r_server.set('ir_s', new_sweeps_str)

        if verbose:
            print(new_sweeps)


def do_ir_prox(pins):
    from sensors.sensors import IRSensor
    ir_left = IRSensor(pins[0])
    ir_right = IRSensor(pins[1])

    while True:
        ir_reading_l = ir_left.get_reading()
        ir_reading_r = ir_right.get_reading()
        r_server.set('ir_l', ir_reading_l)
        r_server.set('ir_r', ir_reading_r)

        if verbose:
            print(ir_reading_l, ir_reading_r)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch sensor readings.')
    parser.add_argument('--sensor', dest='sensor', required=True,
                        help='The sensor you want to monitor.',
                        choices=['sonar', 'ir_sweep', 'ir_prox'])
    args = parser.parse_args()

    if args.sensor == 'sonar':
        do_sonar([25, 8])
    elif args.sensor == 'ir_sweep':
        do_ir_sweep('/dev/ttyAMA0')
    elif args.sensor == 'ir_prox':
        do_ir_prox([24, 21])
