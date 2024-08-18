def combat_rules(world, player, options):
    """Defines rules for combat, light, and victory condition."""
    menu = world.get_region("Menu", player)
    diff = options.difficulty
    menu.connect(world.get_region("Victory", player),
                 rule=lambda state: state.has_any(("Sword", "Hammer"), player) and state.has_all(
                     ("DoubleJump", "Dash", "Bash", "Grapple", "Glide", "Burrow", "Launch"), player))

    if diff == 0:  # Moki
        menu.connect(world.get_region("DepthsLight", player),
                     rule=lambda state: state.has_any(("UpperDepths.ForestsEyes", "Flash"), player))
        menu.connect(world.get_region("Combat.Aerial", player),
                     rule=lambda s: s.has_any(("DoubleJump", "Launch"), player))
        menu.connect(world.get_region("Combat.Dangerous", player),
                     rule=lambda s: s.has_any(("DoubleJump", "Dash", "Bash", "Launch"), player))
        menu.connect(world.get_region("Combat.Shielded", player),
                     rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        menu.connect(world.get_region("Combat.Bat", player), rule=lambda s: s.has("Bash", player))
        menu.connect(world.get_region("Combat.Sand", player), rule=lambda s: s.has("Burrow", player))
        menu.connect(world.get_region("BreakCrystal", player),
                     rule=lambda s: s.has_any(("Sword", "Hammer", "Bow"), player))

    if diff == 1:  # Gorlek
        menu.connect(world.get_region("DepthsLight", player),
                     rule=lambda state: state.has_any(("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        menu.connect(world.get_region("Combat.Aerial", player),
                     rule=lambda s: s.has_any(("DoubleJump", "Launch", "Bash"), player))
        menu.connect(world.get_region("Combat.Dangerous", player),
                     rule=lambda s: s.has_any(("DoubleJump", "Dash", "Bash", "Launch"), player))
        menu.connect(world.get_region("Combat.Shielded", player),
                     rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        menu.connect(world.get_region("Combat.Bat", player), rule=lambda s: s.has("Bash", player))
        menu.connect(world.get_region("Combat.Sand", player), rule=lambda s: s.has("Burrow", player))
        menu.connect(world.get_region("BreakCrystal", player),
                     rule=lambda s: s.has_any(("Sword", "Hammer", "Bow", "Shuriken", "Grenade"), player))

    if options.difficulty >= 2:  # Kii
        menu.connect(world.get_region("DepthsLight", player),
                     rule=lambda state: state.has_any(("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        menu.connect(world.get_region("Combat.Aerial", player), rule=lambda s: True)
        menu.connect(world.get_region("Combat.Dangerous", player),
                     rule=lambda s: s.has_any(("DoubleJump", "Dash", "Bash", "Launch"), player))
        menu.connect(world.get_region("Combat.Shielded", player),
                     rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        menu.connect(world.get_region("Combat.Bat", player), rule=lambda s: True)
        menu.connect(world.get_region("Combat.Sand", player), rule=lambda s: s.has("Burrow", player))
        menu.connect(world.get_region("BreakCrystal", player),
                     rule=lambda s: s.has_any(("Sword", "Hammer", "Bow", "Shuriken", "Grenade"), player))

    if options.difficulty == 3:  # Unsafe
        menu.connect(world.get_region("DepthsLight", player),
                     rule=lambda state: state.has_any(("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        menu.connect(world.get_region("Combat.Aerial", player), rule=lambda s: True)
        menu.connect(world.get_region("Combat.Dangerous", player),
                     rule=lambda s: s.has_any(("DoubleJump", "Dash", "Bash", "Launch"), player))
        menu.connect(world.get_region("Combat.Shielded", player),
                     rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        menu.connect(world.get_region("Combat.Bat", player), rule=lambda s: True)
        menu.connect(world.get_region("Combat.Sand", player), rule=lambda s: s.has("Burrow", player))
        menu.connect(world.get_region("BreakCrystal", player),
                     rule=lambda s: s.has_any(("Sword", "Hammer", "Bow", "Shuriken", "Grenade", "Spear"), player))


def glitch_rules(world, player, options):
    """Defines rules for some glitches."""
    menu = world.get_region("Menu", player)
    if options.glitches:
        menu.connect(world.get_region("WaveDash", player), rule=lambda s: s.has_all(("Dash", "Regenerate"), player))
        menu.connect(world.get_region("HammerJump", player), rule=lambda s: s.has_all(("DoubleJump", "Hammer"), player))
        menu.connect(world.get_region("SwordJump", player), rule=lambda s: s.has_all(("DoubleJump", "Sword"), player))
        menu.connect(world.get_region("GlideHammerJump", player), rule=lambda s: s.has_all(("Glide", "Hammer"), player))
    else:
        menu.connect(world.get_region("WaveDash", player), rule=lambda s: True)
        menu.connect(world.get_region("HammerJump", player), rule=lambda s: True)
        menu.connect(world.get_region("SwordJump", player), rule=lambda s: True)
        menu.connect(world.get_region("GlideHammerJump", player), rule=lambda s: True)