from vision.vision_interface import DominoVision

width_game = 218 #236
height_game = 290 #314
area_game = width_game*height_game
domino_vision = DominoVision(visualize=True, verbose=True)

# Probar directamente desde la camara
domino_vision.test_with_video(channel=0, size_mm=area_game)
# domino_vision.view_video(channel=0)