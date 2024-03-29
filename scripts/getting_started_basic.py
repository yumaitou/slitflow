import os

import matplotlib.pyplot as plt

import slitflow as sf

root_dir = "slitflow_tutorial"
project_dir = os.path.join(root_dir, "getting_started_basic")

# Create directories
if not os.path.isdir(root_dir):
    os.makedirs(root_dir)
if not os.path.isdir(project_dir):
    os.makedirs(project_dir)

if __name__ == '__main__':
    # Script must be written inside the "if __name__ == '__main__'"part
    # when using multiprocessing. We recommend always using this structure.

    # === Run using data objects ===
    # Simulate random walks
    D1 = sf.tbl.create.Index()
    D1.run([], {"type": "trajectory", "index_counts": [2, 3],
                "split_depth": 0})
    print(D1.data[0])

    D2 = sf.trj.random.Walk2DCenter()
    D2.run([D1], {"diff_coeff": 0.1, "interval": 0.1, "n_step": 5,
                  "length_unit": "um", "seed": 1, "split_depth": 0})
    print(D2.data[0])

    # Calculate the Mean Square Displacement
    D3 = sf.trj.msd.Each()
    D3.run([D2], {"group_depth": 2, "split_depth": 0})

    D4 = sf.tbl.stat.Mean()
    D4.run([D3], {"calc_col": "msd", "index_cols": [
           "interval"], "split_depth": 0})
    print(D4.data[0])

    # Make a figure image
    D5 = sf.fig.line.Simple()
    D5.run([D4], {"calc_cols": ["interval", "msd"], "err_col": "sem",
                  "group_depth": 0, "split_depth": 0})

    D6 = sf.fig.style.Basic()
    D6.run([D5], {"limit": [-0.01, 0.52, -0.005, 0.205],
                  "tick": [[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                           [0, 0.05, 0.1, 0.15, 0.2]],
                  "label": ["Interval (s)", "MSD (\u03bcm$^{2}$)"],
                  "format": ['%.1f', '%.2f']})

    D7 = sf.fig.figure.ToTiff()
    D7.run([D6], {"split_depth": 0})

    # The following four lines do not work in GUI-disabled environments like
    # Gitpod and Google Colaboratory.
    # If your environment allows separate window display, uncomment below.

    # import matplotlib
    # matplotlib.use('TkAgg')

    plt.close()
    plt.imshow(D7.to_imshow(0))
    plt.axis("off")
    plt.show()

    # === Run using a pipeline ===

    # make and run a pipeline
    PL = sf.manager.Pipeline(project_dir)
    obs_names = ["Sample1"]
    PL.add(sf.tbl.create.Index(), 0, (1, 1), 'channel1', 'index',
           obs_names, [], [],
           {"type": "trajectory", "index_counts": [2, 3], "split_depth": 0})
    PL.add(sf.trj.random.Walk2DCenter(), 0, (1, 2), None, 'trj',
           obs_names, [(1, 1)], [0],
           {"diff_coeff": 0.1, "interval": 0.1, "n_step": 5,
            "length_unit": "um", "seed": 1, "split_depth": 0})
    PL.add(sf.trj.msd.Each(), 0, (1, 3), None, 'msd',
           obs_names, [(1, 2)], [0],
           {"group_depth": 2, "split_depth": 0})
    PL.add(sf.tbl.stat.Mean(), 0, (1, 4), None, 'avemsd',
           obs_names, [(1, 3)], [0],
           {"calc_col": "msd", "index_cols": ["interval"], "split_depth": 0})
    PL.add(sf.fig.line.Simple(), 0, (1, 5), None, 'msd_fig',
           obs_names, [(1, 4)], [0],
           {"calc_cols": ["interval", "msd"], "err_col": "sem",
            "group_depth": 0, "split_depth": 0})
    PL.add(sf.fig.style.Basic(), 0, (1, 6), None, 'msd_style',
           obs_names, [(1, 5)], [0],
           {"limit": [-0.01, 0.52, -0.005, 0.205],
           "tick": [[0, 0.1, 0.2, 0.3, 0.4, 0.5], [0, 0.05, 0.1, 0.15, 0.2]],
            "label": ["Interval (s)", "MSD (\u03bcm$^{2}$)"],
            "format": ['%.1f', '%.2f']})
    PL.add(sf.fig.figure.ToTiff(), 0, (1, 7), None, 'msd_img',
           obs_names, [(1, 6)], [0],
           {"split_depth": 0})
    PL.save("pipeline")
    PL.run()

    PL.make_flowchart("pipeline", "grp_ana")
