def end_screen(screen_name, co2_consumed, travel_distance, starting_location,
               s_planes_used, m_planes_used, l_planes_used):
    # TODO näytä vanhat tiedot
    print(f"Name: {screen_name}.")
    print(f"Consumed co2 {float(co2_consumed):.2f} tons.")
    print(f"Player {screen_name} travelled {travel_distance}km.")
    print(f"Player {screen_name} started game from {starting_location}.")
    print(f"Player {screen_name} used {s_planes_used} light planes.")
    print(f"Player {screen_name } used {m_planes_used} mid-size planes.")
    print(f"Player {screen_name} used {l_planes_used} Jumbo jets.")
    return
