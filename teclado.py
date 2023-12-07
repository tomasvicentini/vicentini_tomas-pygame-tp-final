    def manejar_eventos_teclado(self):  # Eventos del jugador
        keys = pygame.key.get_pressed()  
        is_moving_previous = self.is_moving
        self.is_moving = (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT])

        if self.on_ladder:
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.up_images) * self.animation_speed_move)
                self.image = self.up_images[self.animacion_contador // self.animation_speed_move]
                self.lock_ladder = True
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.up_images) * self.animation_speed_move)
                self.image = self.up_images[self.animacion_contador // self.animation_speed_move]
                self.lock_ladder = True

        else:
            # Verificar si el jugador está en el suelo
            on_floor = False
            for floor_rect in self.floor_class:
                if self.rect.colliderect(floor_rect):
                    on_floor = True
                    break

            if on_floor:
                ground_level = floor_rect.top - self.rect.height
                if self.rect.y < ground_level:
                    self.rect.y = ground_level  # Ajusta la posición al nivel del suelo
                    self.on_floor = True
                    self.is_jumping = False
                    self.gravity = self.jump_height
                    self.lock_ladder = False
                elif self.rect.y > ground_level:
                    self.rect.y = ground_level  # Ajusta la posición al nivel del suelo
            else:
                self.on_floor = False
        
        if not self.lock_ladder:    
            if self.is_moving:
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.move_images) * self.animation_speed_move)

            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
                self.image = self.move_images[self.animacion_contador // self.animation_speed_move]
                self.move_right = True
            elif keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
                self.image = pygame.transform.flip(self.move_images[self.animacion_contador // self.animation_speed_move], True, False)
                self.move_right = False
            else:
                if self.move_right:
                    self.animacion_contador = (self.animacion_contador + 1) % (len(self.idle_images) * self.animation_speed_idle)
                    self.image = self.idle_images[self.animacion_contador // self.animation_speed_idle]
                else:
                    self.animacion_contador = (self.animacion_contador + 1) % (len(self.idle_images) * self.animation_speed_idle)
                    self.image = pygame.transform.flip(self.idle_images[self.animacion_contador // self.animation_speed_idle], True, False)
                
                if not is_moving_previous:
                    self.image = pygame.transform.flip(self.image, keys[pygame.K_LEFT], False)

            if keys[pygame.K_SPACE] and not self.is_jumping:
                self.is_jumping = True

            if self.is_jumping:
                self.y_initial = self.rect.y
                flag = True
                if self.move_right:
                    self.image = self.jump_images[0]
                else:
                    self.image = pygame.transform.flip(self.jump_images[0], True, False)   
                if self.gravity >= -self.jump_height:
                    neg = 1
                    if self.gravity < 0:
                        neg = -1
                    if flag==True or not self.rect.y == self.y_initial:
                        self.rect.y -= (self.gravity ** 2) * 0.25 * neg
                        self.gravity -= 1
                        flag = False
                else:
                    if self.move_right:
                        self.image = self.jump_images[-1]
                    else:
                        self.image = pygame.transform.flip(self.jump_images[-1], True, False)   
                    self.is_jumping = False
                    self.gravity = self.jump_height 

            if keys[pygame.K_LCTRL] and not self.space_pressed and not self.is_jumping:
                self.shoot_laser()
                self.space_pressed = True
                self.ready = False
                self.laser_time = pygame.time.get_ticks()
                if self.move_right:
                    self.animacion_contador = (self.animacion_contador + 1) % (len(self.fire_images) * self.animation_speed_fire)
                    self.image = self.fire_images[self.animacion_contador // self.animation_speed_fire]                
                else:
                    self.animacion_contador = (self.animacion_contador + 1) % (len(self.fire_images) * self.animation_speed_fire)
                    self.image = pygame.transform.flip(self.fire_images[self.animacion_contador // self.animation_speed_fire], True, False)    

        if not keys[pygame.K_LCTRL]:
            self.space_pressed = False     


