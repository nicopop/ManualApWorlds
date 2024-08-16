from worlds.generic.Rules import add_rule


def combat_rules(world, player, options):
    add_rule(world.get_location("Combat.Aerial", player), lambda s: s.has_any(("DoubleJump", "Launch"), player))
    add_rule(world.get_location("Combat.Dangerous", player), lambda s: s.has_any(("DoubleJump", "Dash", "Bash", "Launch"), player))
    add_rule(world.get_location("Combat.Shielded", player), lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
    add_rule(world.get_location("Combat.Bat", player), lambda s: s.has("Bash", player))
    add_rule(world.get_location("Combat.Sand", player), lambda s: s.has("Burrow", player))
    add_rule(world.get_location("BreakCrystal", player), lambda s: s.has_any(("Sword", "Hammer", "Bow"), player))
    if options.difficulty >= 1:  # Gorlek
        add_rule(world.get_location("Combat.Aerial", player), lambda s: s.has("Bash", player))
        add_rule(world.get_location("BreakCrystal", player), lambda s: s.has_any(("Shuriken", "Grenade"), player))
    if options.difficulty >= 2:  # Kii
        add_rule(world.get_location("Combat.Aerial", player), lambda s: True)
        add_rule(world.get_location("Combat.Bat", player), lambda s: True)
    if options.difficulty == 3:  # Unsafe
        add_rule(world.get_location("BreakCrystal", player), lambda s: s.has("Spear", player))


def glitch_rules(world, player):
    add_rule(world.get_location("WaveDash", player), lambda s: s.has_all(("Dash", "Regenerate"), player))
    add_rule(world.get_location("HammerJump", player), lambda s: s.has_all(("DoubleJump", "Hammer"), player))
    add_rule(world.get_location("SwordJump", player), lambda s: s.has_all(("DoubleJump", "Sword"), player))
    add_rule(world.get_location("GlideHammerJump", player), lambda s: s.has_all(("Glide", "Hammer"), player))
