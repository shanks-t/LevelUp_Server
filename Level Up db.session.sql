         select g.title, u.first_name, u.last_name, ga.id
            from game g
                join gamer ga
                on g.gamer_id = ga.id
                join user u
                on ga.user_id = u.id