## X-Mas tree in Blender

This is a simulation of Matt Parker's Christmas tree in Blender 2.91. It is meant to allow other people to test and debug their LED patterns without having the real tree available. For now, it only contains the LEDs in the correct locations, but not the tree branches.

To run the simulation, open the .blend file in Blender, go to the Scripting workspace and run the blender.py script. It will load the original file by Matt Parker and patch it so it controls the virtual tree as if it were the real tree. Make sure to switch to rendered mode first to see the colors.

This project was organized so as to make as few changes as possible to the original file. However, a few small changes were needed:

- The xmaslight() function was moved into an if statement so it does not run immediately when the module is imported (it will still run if the module is executed directly).
- The run flag was moved outside the function so we can stop it from outside, otherwise it would run forever until we force-quit Blender.
- The path to the LED coordinates file was moved outside the function to allow us to inject the path relative to the Blender file, otherwise the script would not be able to find it when running from Blender.

These changes should not change the behavior of the script when running outside of Blender. However, note that the neopixel and board files must be removed before the script can be run on the actual tree.
