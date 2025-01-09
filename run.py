
from src.tournament.scheduler import create_schedule, generate_pool_gantt

def main():
    schedules = {
        'A': {
            'ALLER': 21,   # 21h00
            'RETOUR': 21.5,  # 21h30
        },
        'B': {
            'ALLER': 21,   # 21h00
            'RETOUR': 21.5,  # 21h30
        }
    }
    
    # Store schedules by pool
    pool_schedules = {}
    
    for pool, phases in schedules.items():
        pool_schedules[pool] = {}
        for phase, start_hour in phases.items():
            schedule = create_schedule(pool, start_hour, phase)
            pool_schedules[pool][phase] = schedule
        
        # Generate combined Gantt chart for each pool with start time
        generate_pool_gantt(pool_schedules[pool], pool, start_hour=phases['ALLER'])

if __name__ == "__main__":
    main()
