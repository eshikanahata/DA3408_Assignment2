# DA3408 Assignment 2

## Repository Structure

* **`q1/`**: Contains the code and Dockerfiles (naive and multi-stage) for the single container Spam Detection API.

* **`q2/`**: Contains the Docker Compose configuration to run the API alongside a Redis caching layer.

* **`q3/`**: Contains the scripts to generate data shards and the Kubernetes manifest for parallel batch validation.

* **`q4/`**: Contains the Kubernetes `deployment.yaml` and `service.yaml` manifests for the API, along with a `v2/` directory for demonstrating rolling updates.

* **`evidence/`**: Contains CLI outputs validating image sizes, cache speedups, pod scaling, and rollout statuses.

* **`writeup.pdf`**: The report containing answers to conceptual questions from the assignment. 

## How to Reproduce Results

### Prerequisites

You will need Docker, Docker Compose, a local Kubernetes cluster (like minikube or kind), and `kubectl` installed on your machine.

### Question 1: Single Stage vs. Multi Stage Docker

1. Navigate to the `q1/` directory.

2. Train the model and generate the dataset:

   ```
   python train.py
   
   ```

3. Build the naive image:

   ```
   docker build -t spam-api:naive -f Dockerfile.naive .
   
   ```

4. Build the multi-stage image:

   ```
   docker build -t spam-api:multistage -f Dockerfile .
   
   ```

5. Compare the image sizes using `docker images` 

### Question 2: Multi Container Orchestration 

1. Navigate to the `q2/` directory.

2. Train the model:

   ```
   python train.py
   
   ```

3. Start the services (API and cache) using Docker Compose:

   ```
   docker compose up -d
   
   ```

4. Send repeated POST requests to the `/predict` endpoint to observe the cache hit speedup.

5. Tear down the stack:

   ```
   docker compose down
   
   ```

### Question 3: Kubernetes Indexed Job

1. Navigate to the `q3/` directory.

2. Generate the 8 data shards:

   ```
   python generate_shards.py
   
   ```

3. Build the validation image and load it into your Kubernetes cluster

4. Apply the job manifest:

   ```
   kubectl apply -f indexed-job.yaml
   
   ```

5. Verify parallelism and review logs for invalid row counts

   ```
   kubectl get pods -o wide
   kubectl logs -l job-name=data-validator
   
   ```

### Question 4: Kubernetes Deployments 

1. Navigate to the `q4/` directory.

2. Apply the initial deployment and service:

   ```
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   
   ```

3. **Test Self-Healing**: Delete a running pod manually and observe the ReplicaSet instantly recreating it 

4. **Test Rolling Update**: Apply the updated manifests from the `v2/` directory:

   ```
   kubectl apply -f v2/deployment.yaml
   
   ```

5. Monitor the rollout status without downtime:

   ```
   kubectl rollout status deployment/spam-api-deployment
   kubectl rollout history deployment/spam-api-deployment
   
   ```