select g.*, (u.first_name ||' ' ||u.last_name) as full_name, ga.id as game_type_id
        from levelupapi_game g
            join levelupapi_gamer ga
            on g.gamer_id = ga.id
            join auth_user u
            on ga.user_id = u.id


select e.*, (u.first_name ||' ' ||u.last_name) as full_name
    from levelupapi_event e
        join levelupapi_eventgamer eg
            on e.id = eg.event_id
        join levelupapi_gamer ga
            on eg.gamer_id = ga.id
        join auth_user u
            on ga.user_id = u.id