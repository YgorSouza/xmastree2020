import os
import bpy

finished = True

class FinishedException(Exception):
    pass

def raise_if_finished():
    if finished:
        raise FinishedException()

coords_file_path = os.path.join(os.path.dirname(bpy.data.filepath),"coords.txt")

def load_coordinates():
    import sys
    with open(coords_file_path) as coords_file:
        get_coords = lambda line: tuple([float(i)/100 for i in line.strip().strip("[]").split(',')])
        return [get_coords(line) for line in coords_file]

def create_objects(coords):
    # Delete all objects 
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    #Delete all materials
    [bpy.data.materials.remove(bpy.data.materials[k]) for k in bpy.data.materials.keys()]

    for i, loc in enumerate(coords):
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=loc)
        bpy.context.active_object.name =f"LED.{i}"
        mat = bpy.data.materials.new(name=bpy.context.active_object.name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.remove(mat.node_tree.nodes[0])
        emission = nodes.new("ShaderNodeEmission")
        links.new(emission.outputs[0], nodes["Material Output"].inputs[0])
        nodes["Emission"].inputs[0].default_value=(1,1,1,1)
        bpy.context.active_object.active_material = mat

def set_color(index, r,g,b,a):
    obj = bpy.data.objects[f"LED.{index}"]
    emission = obj.active_material.node_tree.nodes["Emission"]
    emission.inputs[0].default_value=(r,g,b,a)

class NeoPixel:
    def __init__(self, pin=None, pixel_count=None, auto_write=True):
        self.window_redraw_count = 0
        self.auto_write = auto_write
        coords = load_coordinates()
        test_obj = f"LED.{len(coords)-1}"
        if test_obj not in bpy.data.objects.keys():
            create_objects(coords)

    def __setitem__(self, index, value):
       raise_if_finished()
       g,r,b = value
       set_color(index,r/255, g/255, b/255, 1)
       if self.auto_write:
           self.force_window_redraw()

    def force_window_redraw(self):
        self.window_redraw_count += 1
        if self.window_redraw_count > 20:
            self.window_redraw_count = 0
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def show(self):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

def test_module():
    import random
    import time
    pixels = NeoPixel()
    for tick in range(20):
        for i in range(500):
            hue = random.randint(1,6)
            r = hue & 0b100 and 255 or 0
            g = hue & 0b010 and 255 or 0
            b = hue & 0b001 and 255 or 0
            pixels[i] = [g,r,b]
        time.sleep(0.1)
    finished = True

if __name__ == "__main__":
    finished = False
    test_module()
