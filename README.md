# Flask Project Setup


## Prerequisites

Make sure you have the following installed on your machine:
- Python (>= 3.6)
- Git

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine using Git:

```sh
git clone https://github.com/2307prashant/quickbook-sample
cd quickbook-sample
```

### 2. Creating a virtual environment

Run, the following command to create a virtual environment

```py
python -m venv venv
```

Then, run the following command to activate the virtual environment

```
env\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using pip:

```py
pip install -r requirements.txt
```

### 4. Configure Environment Variables

- Copy the `.env.sample` file to `.env`
- Add your `CLIENT_ID` and `CLIENT_SECRET` in the `.env` file

### 5. Run the application

```py
python app.py
```

The app should be accessible at [http://localhost:5000/app](http://localhost:5000/app)
