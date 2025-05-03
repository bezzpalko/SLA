# Simulation and Reliability Analysis of a Repairable System Model of a Data Center, SLA

This project simulates the operational characteristics of a server room, including server failures, repairs, and maintenance. The simulation is based on a Weibull distribution for failure times and an exponential distribution for repair times. It is designed to model different service level agreements (SLAs) and evaluate performance using Monte Carlo simulations.

## Features

- **Server Failure Simulation**: Each server has a failure time drawn from a Weibull distribution.
- **Repair Process**: Repairs are modeled as an exponential process with a specified repair rate.
- **Metrics Calculation**: Calculates key performance metrics such as:
  - Mean Time Between Failures (MTBF)
  - Mean Time To Repair (MTTR)
  - System Availability
- **Monte Carlo Simulation**: Runs multiple trials to estimate the probability distribution of availability and other performance metrics.
- **Service Level Agreements**: Supports multiple SLAs, each with different performance requirements and penalties.

## Structure

### `ServerRoom` Class
The main class for simulating the server room.

It defines:
- The number of servers
- Parameters for failure times (Weibull distribution)
- Repair parameters
- It calculates performance metrics based on these parameters.

### `simulate_server_room` Function
Runs the simulation for the server room, updating the status of servers at each time step.

### `analyze_results` Function
Analyzes the simulation results, calculating metrics such as:
- Availability
- Mean Time Between Failures (MTBF)
- Mean Time To Repair (MTTR)
- Total repairs and downtime

### `monte_carlo_simulation` Function
Performs a Monte Carlo simulation to assess the statistical characteristics and success rate based on multiple simulations.

## Service Level Parameters

The project supports three service levels:

### Standard
- **Availability**: 95%
- **Max Repairs**: 70
- **Max Downtime**: 400 hours
- **Maintenance Cost**: $430,000

### Premium
- **Availability**: 99%
- **Max Repairs**: 30
- **Max Downtime**: 80 hours
- **Maintenance Cost**: $915,000

### Ultra Premium
- **Availability**: 99.5%
- **Max Repairs**: 15
- **Max Downtime**: 40 hours
- **Maintenance Cost**: $2,300,000

## Installation

To run the simulation, you'll need to have the following Python packages installed:

- `numpy`
- `matplotlib`
