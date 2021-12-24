import pyqtgraph.opengl as gl
from opensimplex import OpenSimplex
import numpy as np


class Mesh:

    # self.window.addItem(self.view1)
    def __init__(self, rate):
        # pass

        # get dimensions
        # data_points = rate/2
        dim_x = int(np.sqrt(rate))
        while True:
            dim_y = rate / dim_x
            if dim_y.is_integer() and dim_y * dim_x == rate:
                self._dim_x = dim_x
                self._dim_y = dim_y
                break

            else:
                dim_x += 1

        # constants and arrays
        self.rate = rate
        self.offset = 0
        self.ypoints = np.arange(-20, 20, 40 / self._dim_y)
        self.xpoints = np.arange(-20, 20, 40 / self._dim_x)
        self.nxfaces = len(self.xpoints)
        self.nyfaces = len(self.ypoints)

        self.RATE = rate
        self.CHUNK = len(self.xpoints) * len(self.ypoints)
        # add noise
        self.noise = OpenSimplex()

        # create the veritices array
        verts, faces, colors = self._build_mesh()

        self.view = gl.GLMeshItem(
            faces=faces,
            vertexes=verts,
            faceColors=colors,
            drawEdges=True,
            smooth=False,
            edgeColor=(0, 0, 0, 1),
        )
        self.view.setGLOptions("additive")

    def _build_mesh(self, offset=0, height=2.5, wf_data=None):
        if wf_data is not None:
            wf_data = np.array(wf_data)

            wf_data = wf_data * 0.01
            wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))
        else:
            wf_data = np.array([1] * self.rate)
            wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))

        faces = []
        colors = []
        verts = np.array(
            [
                [
                    x,
                    y,
                    wf_data[xid][yid]
                    * self.noise.noise2d(x=xid / 5 + offset, y=yid / 5 + offset),
                ]
                for xid, x in enumerate(self.xpoints)
                for yid, y in enumerate(self.ypoints)
            ]
        )

        for yid in range(self.nyfaces - 1):
            yoff = yid * self.nxfaces
            for xid in range(self.nxfaces - 1):
                faces.append(
                    [
                        xid + yoff,
                        xid + yoff + self.nyfaces,
                        xid + yoff + self.nyfaces + 1,
                    ]
                )
                faces.append(
                    [xid + yoff, xid + yoff + 1, xid + yoff + self.nyfaces + 1,]
                )
                colors.append(
                    [
                        np.random.randint(0, 168),
                        np.random.randint(0, 168),
                        np.random.randint(0, 168),
                        0.5,
                    ]
                )
                colors.append(
                    [
                        np.random.randint(0, 168),
                        np.random.randint(0, 168),
                        np.random.randint(0, 168),
                        0.5,
                    ]
                )

        faces = np.array(faces, dtype=np.uint32)
        colors = np.array(colors, dtype=np.float32)

        return verts, faces, colors

    def update(self, data):
        """
        update the mesh and shift the noise each time
        """
        verts, faces, colors = self._build_mesh(offset=self.offset, wf_data=data)
        self.view.setMeshData(vertexes=verts, faces=faces, faceColors=colors)
        self.offset -= 0.05
