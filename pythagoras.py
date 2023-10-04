import sys
import pygame as pg
import numpy as np


class Simulation:
    def __init__(self, shapes):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(screen_size)
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.screen.fill(pg.Color('black'))
        self.shapes = shapes
        self.generation_counter = -1
        self.is_increasing_generations = True
        print('hello')

    def update(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.logic()
            self.screen.fill(pg.Color('black'))
            self.draw()
            pg.display.update()
            self.clock.tick(3)

    def logic(self):
        if self.is_increasing_generations:
            self.generation_counter += 1
            if self.generation_counter >= max_generations:
                self.is_increasing_generations = False
        else:
            self.generation_counter -= 1
            if self.generation_counter <= 0:
                self.is_increasing_generations = True

    def draw(self):
        for shape in self.shapes:
            shape.draw(self.screen, self.generation_counter)


class Pythagorean:
    def __init__(self, vertices, angle=np.radians(45), generation=0):
        self.vertices = vertices
        self.angle = angle
        self.s = []
        self.children = []
        self.generation = generation
        self.color = 0
        if self.generation > 6:
            self.color = np.array([85, 107, 47])
        else:
            self.color = np.array([101, 67, 33])

        if self.generation < 6:
            self.color = np.array([101, 67, 33])
        elif self.generation < 10:
            self.color = np.array([255, 64, 160])
        else:
            self.color = np.array([255, 153, 204])

        if generation < max_generations:
            self.find_new_vertices()

    def find_new_vertices(self):
        # Calculate Common Vertex
        upper_side_vector = (self.vertices[2] - self.vertices[1])
        rot = self.rotation_matrix(self.angle)
        common_vertex = np.matmul(upper_side_vector * np.cos(self.angle), rot) + self.vertices[1]

        # Calculate First Child Vertices
        bottom_line_vector = common_vertex - self.vertices[1]
        rot = self.rotation_matrix(np.pi / 2)
        vertex1 = np.matmul(bottom_line_vector, rot) + self.vertices[1]
        vertex2 = vertex1 + common_vertex - self.vertices[1]

        # Calculate Second Child Vertices
        bottom_line_vector = self.vertices[2] - common_vertex
        rot = self.rotation_matrix(np.pi / 2)
        vertex3 = np.matmul(bottom_line_vector, rot) + self.vertices[2]
        vertex4 = common_vertex + vertex3 - self.vertices[2]

        # Create New Generation
        child1_vertices = np.array([self.vertices[1], vertex1, vertex2, common_vertex])
        child2_vertices = np.array([common_vertex, vertex4, vertex3, self.vertices[2]])
        self.children = [Pythagorean(child1_vertices, self.angle, self.generation+1),
                         Pythagorean(child2_vertices, self.angle, self.generation+1)]
        self.s = [common_vertex, self.vertices[2], vertex3, vertex4, self.vertices[1], vertex2, vertex1]

    def draw(self, screen, target_generation):
        if self.generation <= target_generation:
            pg.draw.line(screen, self.color, self.vertices[0], self.vertices[1], 1)
            pg.draw.line(screen, self.color, self.vertices[1], self.vertices[2], 1)
            pg.draw.line(screen, self.color, self.vertices[2], self.vertices[3], 1)
            pg.draw.line(screen, self.color, self.vertices[3], self.vertices[0], 1)
            if self.children:
                for child in self.children:
                    child.draw(screen, target_generation)

        # for s in self.s:
        #     pg.draw.circle(screen, pg.Color('red'), s, 3)

    @staticmethod
    def rotation_matrix(angle):
        rot = np.array([[np.cos(angle), -np.sin(angle)],
                        [np.sin(angle), np.cos(angle)]])
        return rot


if __name__ == '__main__':
    screen_size = np.array([1000, 640])
    max_generations = 15
    # pythagorean1 = Pythagorean(np.array([[280, 600], [280, 400], [360, 400], [360, 600]]), angle=np.radians(40))
    # pythagorean2 = Pythagorean(np.array([[680, 600], [680, 500], [760, 500], [760, 600]]), angle=np.radians(40))
    pythagorean1 = Pythagorean(np.array([[1200, 1400], [1200, 800], [1360, 800], [1360, 1400]]), angle=np.radians(30))
    simulation = Simulation([pythagorean1])
    simulation.update()

