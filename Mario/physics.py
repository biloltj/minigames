def resolve_collisions(player, platforms):
    player.on_ground = False

    for p in platforms:
        if player.rect.colliderect(p):
            if player.vel_y > 0:
                player.rect.bottom = p.top
                player.vel_y = 0
                player.on_ground = True
            elif player.vel_y < 0:
                player.rect.top = p.bottom
                player.vel_y = 0
