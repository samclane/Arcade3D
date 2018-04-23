import arcade

import wireframe


class ProjectionViewer(arcade.Window):
    """ Displays 3D objects on an Arcade screen."""

    def __init__(self, width, height):
        super().__init__(width, height)
        self.width = width
        self.height = height
        self.set_caption('Wireframe Display')
        self.background = (10, 10, 50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255, 255, 255)
        self.edgeColour = (200, 200, 200)
        self.nodeRadius = 4

    def setup(self):
        # Create your sprites and sprite lists here
        arcade.set_background_color(self.background)
        self.flip()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        for wf in self.wireframes.values():
            if self.displayEdges:
                for edge in wf.edges:
                    arcade.draw_line(edge.start.x, edge.start.y, edge.stop.x, edge.stop.y, self.edgeColour, 1)

            if self.displayNodes:
                for node in wf.nodes:
                    arcade.draw_circle_filled(node.x, node.y, self.nodeRadius, self.nodeColour)

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def addWireframe(self, name, wf):
        """ Add a named wireframe object. """
        self.wireframes[name] = wf

    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        for wf in self.wireframes.values():
            wf.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """

        centre_x = self.width / 2
        centre_y = self.height / 2

        for wf in self.wireframes.values():
            wf.scale(centre_x, centre_y, scale)

    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """

        rotateFunction = 'rotate' + axis

        for wf in self.wireframes.values():
            centre = wf.findCentre()
            getattr(wf, rotateFunction)(*centre, theta)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.translateAll('x', -10)
        elif symbol == arcade.key.RIGHT:
            self.translateAll('x', 10)
        elif symbol == arcade.key.DOWN:
            self.translateAll('y', -10)
        elif symbol == arcade.key.UP:
            self.translateAll('y', 10)
        elif symbol == arcade.key.EQUAL:
            self.scaleAll(1.25)
        elif symbol == arcade.key.MINUS:
            self.scaleAll(.8)
        elif symbol == arcade.key.Q:
            self.rotateAll('X', 0.1)
        elif symbol == arcade.key.W:
            self.rotateAll('X', -0.1)
        elif symbol == arcade.key.A:
            self.rotateAll('Y', 0.1)
        elif symbol == arcade.key.S:
            self.rotateAll('Y', -0.1)
        elif symbol == arcade.key.Z:
            self.rotateAll('Z', 0.1)
        elif symbol == arcade.key.X:
            self.rotateAll('Z', -0.1)


if __name__ == "__main__":
    pv = ProjectionViewer(400, 300)

    cube = wireframe.Wireframe()
    cube.addNodes([(x, y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)])
    cube.addEdges(
        [(n, n + 4) for n in range(0, 4)] + [(n, n + 1) for n in range(0, 8, 2)] + [(n, n + 2) for n in (0, 1, 4, 5)])

    pv.addWireframe('cube', cube)
    pv.setup()
    arcade.run()
