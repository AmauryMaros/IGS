# Use a base image that supports both Python and R
FROM rocker/r-ver:4.2.3

# Install Python
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Streamlit and other required Python packages
RUN pip3 install --no-cache-dir streamlit boto3

# Install R packages
RUN R -e "install.packages('shiny')"
RUN R -e "install.packages('ggplot2')"
RUN R -e "install.packages('dplyr')"

# Set the working directory
WORKDIR /app

# Copy your app files into the container
COPY . /app

# Expose the port Streamlit will use
EXPOSE 8501

# Command to run Streamlit app
CMD ["streamlit", "run", "your_app.py"]
