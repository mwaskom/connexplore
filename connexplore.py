#! /usr/bin/env python
import numpy as np
import pandas as pd
from surfer import Brain


class ConnectivityExplorer(Brain):

    hemis = ["lh", "rh"]
    _colorbars = []

    def __init__(self, matrix, names, annot=None, vlim=.7,
                 subject="fsaverage", surface="inflated", size=700,
                 **kwargs):
        """Initialize the interactive object."""
        super(ConnectivityExplorer, self).__init__(
            subject, "split", surface,
            config_opts={"width": size * 2, "height": size},
            **kwargs
            )

        if annot is not None:
            self.add_annotation(annot, borders=True, alpha=.75)

        self.matrix = matrix
        self.names = names
        self.cmap = "RdBu_r"
        self.vlim = vlim

        for i, hemi in enumerate(self.hemis):

            # Set the correct callback function for each hemisphere
            f = self._figures[0][i]
            f.on_mouse_pick(self._picker_factory(hemi), button="Right")

            # Start with a blank (white) statistical map
            self._update_stat_map(np.zeros(len(names)), hemi)

    def _update_stat_map(self, stat_map, hemi):
        """Plot the statistic values within each region."""
        self.add_data(stat_map, -self.vlim, self.vlim,
                      colormap=self.cmap, colorbar=True, hemi=hemi,
                      remove_existing=True)
        self._colorbars.extend(self.data_dict[hemi]["colorbars"])

    def _update_mask(self, mask_data, hemi):
        """Mark vertices within the seed region or with missing data."""
        cmap = [(0, 0, 0), (.5, .5, .5), (1, .94, .65)]
        self.add_data(mask_data, 0, 2, .5, cmap,
                      colorbar=False, remove_existing=False, hemi=hemi)

    def _update_focus(self, vertex, hemi):
        """Plot a spherical glyph at the clicked vertex."""
        while self.foci_dict:
            self.foci_dict.popitem()[1][0].remove()
        self.add_foci([vertex], coords_as_verts=True,
                      color=(1, .94, .65), hemi=hemi)

    def _clear_colorbars(self):

        while self._colorbars:
            self._colorbars.pop().visible = False

    def _picker_factory(self, pick_hemi):
        """Generate a hemisphere-specific picker callback."""
        def _picker(p):
            """Add connectivity information based on clicked point."""
            # Remove older colorbars
            self._clear_colorbars()

            # Get the name for the ROI that was clicked
            seed_name = self.names.loc[p.point_id, pick_hemi]

            # Plot the clicked vertex
            self._update_focus(p.point_id, pick_hemi)

            for hemi in self.hemis:

                try:
                    # Pull out the connectivity vector between the
                    # clicked region and all regions in this hemi
                    stats = self.matrix.filter(regex=hemi).loc[seed_name]

                    # Assign the stats to each vertex in the mesh
                    stat_map = stats.loc[self.names[hemi]]

                    # Plot the statistic values in each region
                    self._update_stat_map(stat_map.fillna(0).values, hemi)

                except KeyError:
                    # The click was outside of where we have data
                    stat_map = pd.Series([np.nan] * len(self.names))

                # Get a map of all vertices where we lack data
                mask_data = stat_map.isnull().astype(int).values

                if hemi == pick_hemi:
                    # Add in vertices from the seed region
                    mask_data += (self.names[hemi] == seed_name) * 2

                # Plot the missing map and seed highlight
                self._update_mask(mask_data, hemi)

        return _picker


if __name__ == "__main__":

    try:
        get_ipython

        import sys
        from argparse import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument("matrix")
        parser.add_argument("names")
        parser.add_argument("-annot")
        args = parser.parse_args(sys.argv[1].split())

        matrix = pd.read_csv(args.matrix, index_col=0)
        names = pd.read_csv(args.names)

        c = ConnectivityExplorer(matrix, names, args.annot)

    except NameError:

        import os
        import sys

        args = " ".join(sys.argv[1:])
        cmd = "ipython -i --gui=qt -- {} '{}'".format(__file__, args)
        os.system(cmd)