for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_x:
                                    pygame.mixer.music.set_volume(0)
                                elif event.key == pygame.K_z:
                                    pygame.mixer.music.set_volume(0.5)