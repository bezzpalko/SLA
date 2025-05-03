import numpy as np
import matplotlib.pyplot as plt


# Server Room simulation class
class ServerRoom:
    def __init__(self, num_servers, weibull_shape, weibull_scale, repair_rate):
        self.num_servers = num_servers
        self.weibull_shape = weibull_shape
        self.weibull_scale = weibull_scale
        self.repair_rate = repair_rate

        self.servers_status = np.ones(num_servers)  # 1 means operational, 0 means failed
        self.time_to_failure = self.sample_failure_times()  # Time to failure for each server
        self.time_to_repair = np.zeros(num_servers)  # Repair times for servers

        self.total_downtime = 0  # Total downtime
        self.total_repairs = 0  # Total repairs performed
        self.total_uptime = 0  # Total uptime (for MTBF calculation)

    def sample_failure_times(self):
        # Generate failure times for servers from Weibull distribution
        return np.random.weibull(self.weibull_shape, self.num_servers) * self.weibull_scale

    def sample_repair_time(self):
        # Repairs modeled as an exponential process
        return np.random.exponential(1 / self.repair_rate)

    def update_failure_and_repair(self, current_time, time_step):
        downtime_flag = False
        for i in range(self.num_servers):
            if self.servers_status[i] == 1:
                if self.time_to_failure[i] <= current_time:
                    self.servers_status[i] = 0
                    self.time_to_repair[i] = current_time + self.sample_repair_time()  # Assign repair time
            else:
                downtime_flag = True
                if self.time_to_repair[i] <= current_time:
                    self.servers_status[i] = 1
                    self.time_to_failure[i] = current_time + np.random.weibull(
                        self.weibull_shape) * self.weibull_scale
                    self.total_repairs += 1

        if downtime_flag:
            self.total_downtime += time_step
        else:
            self.total_uptime += time_step

    def calculate_mtbf(self, total_time):
        # Calculate Mean Time Between Failures (MTBF)
        return self.total_uptime / self.total_repairs if self.total_repairs > 0 else total_time

    def calculate_mttr(self):
        # Calculate Mean Time To Repair (MTTR)
        return self.total_downtime / self.total_repairs if self.total_repairs > 0 else 0

    def calculate_availability(self, total_time):
        # Calculate system availability
        mtbf = self.calculate_mtbf(total_time)
        mttr = self.calculate_mttr()
        return mtbf / (mtbf + mttr) if (mtbf + mttr) > 0 else 0


def simulate_server_room(num_servers, weibull_shape, weibull_scale, repair_rate, time_horizon, time_step):
    server_room = ServerRoom(num_servers, weibull_shape, weibull_scale, repair_rate)

    current_time = 0
    while current_time < time_horizon:
        server_room.update_failure_and_repair(current_time, time_step)
        current_time += time_step
    return server_room


def analyze_results(server_room, time_horizon, service_level):
    availability = server_room.calculate_availability(time_horizon) * 100
    mtbf = server_room.calculate_mtbf(time_horizon)
    mttr = server_room.calculate_mttr()
    total_repairs = server_room.total_repairs
    total_downtime = server_room.total_downtime

    maintenance_cost = service_level['maintenance_cost']
    penalty = service_level['penalty'] if availability < service_level['availability'] else 0

    return {
        "availability": availability,
        "mtbf": mtbf,
        "mttr": mttr,
        "total_repairs": total_repairs,
        "total_downtime": total_downtime,
        "cost": maintenance_cost + penalty,
        "penalty": penalty,
    }


# Service level parameters
service_levels = {
    "standard": {
        "availability": 95,
        "max_repairs": 70,
        "max_downtime": 400,
        "maintenance_cost": 430000,
        "penalty": 100000,
    },
    "premium": {
        "availability": 99,
        "max_repairs": 30,
        "max_downtime": 80,
        "maintenance_cost": 915000,
        "penalty": 437500,
    },
    "ultra_premium": {
        "availability": 99.5,
        "max_repairs": 15,
        "max_downtime": 40,
        "maintenance_cost": 2300000,
        "penalty": 1250000,
    },
}
# CHOOSE ONE CONTRACT LEVEL AND COMMENT OUT OTHERS
# Parameters for the standard service level
# num_servers = 100
# weibull_shape = 2.0
# weibull_scale = 425 * 24
# repair_rate = 1 / 5
# time_horizon = 8760
# time_step = 1

# Parameters for the premium service level
# num_servers = 100
# weibull_shape = 2.0
# weibull_scale = 800 * 24
# repair_rate = 1 / 2.2
# time_horizon = 8760
# time_step = 1

# Parameters for the ultra premium service level
num_servers = 100
weibull_shape = 2
weibull_scale = 1200 * 24
repair_rate = 1 / 2
time_horizon = 8760
time_step = 1

server_room = simulate_server_room(num_servers, weibull_shape, weibull_scale, repair_rate, time_horizon, time_step)
results = analyze_results(server_room, time_horizon, service_levels['standard'])

print("Results for the standard service level:")
for key, value in results.items():
    print(f"{key}: {value:.2f}")


def monte_carlo_simulation(num_servers, weibull_shape, weibull_scale, repair_rate, time_horizon, time_step, num_trials,
                           service_level):
    mc_results = {
        "availability": [],
        "mtbf": [],
        "mttr": [],
        "total_repairs": [],
        "total_downtime": [],
        "cost": [],
        "penalty": [],
    }
    success_counts = {
        "availability": 0,
        "max_repairs": 0,
        "max_downtime": 0,
    }

    for _ in range(num_trials):
        server_room = simulate_server_room(num_servers, weibull_shape, weibull_scale, repair_rate, time_horizon,
                                           time_step)
        trial_results = analyze_results(server_room, time_horizon, service_level)

        for key in mc_results.keys():
            mc_results[key].append(trial_results[key])

        if trial_results["availability"] >= service_level["availability"]:
            success_counts["availability"] += 1
        if trial_results["total_repairs"] <= service_level["max_repairs"]:
            success_counts["max_repairs"] += 1
        if trial_results["total_downtime"] <= service_level["max_downtime"]:
            success_counts["max_downtime"] += 1

    success_rates = {key: (count / num_trials) * 100 for key, count in success_counts.items()}

    stats = {key: {"mean": np.mean(values), "std": np.std(values)} for key, values in mc_results.items()}
    return mc_results, stats, success_rates


num_trials = 100

mc_results, mc_stats, mc_success_rates = monte_carlo_simulation(
    num_servers,
    weibull_shape,
    weibull_scale,
    repair_rate,
    time_horizon,
    time_step,
    num_trials,
    service_levels['ultra_premium']  # CHANGE CONTRACT NAME FOR CONTROL
)

print("\nMonte Carlo Simulation Results (Standard Service Level):")
for key, value in mc_stats.items():
    print(f"{key}: mean={value['mean']:.2f}, std={value['std']:.2f}")

print("\nSuccess Rates (%):")
for key, rate in mc_success_rates.items():
    print(f"{key}: {rate:.2f}%")

plt.hist(mc_results["availability"], bins=30, edgecolor="black", alpha=0.7)
plt.title("Histogram of Availability (Monte Carlo Simulation)")
plt.xlabel("Availability (%)")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()
