# Running `measureltVnew.py`

To execute the script, use the following command:

```sh
python measureltVnew.py n-pts
```

where `n-pts` is determined by:

```sh
Voltage = 0.01 * n_pts + 0.1
```

The script will automatically generate measurement results.  
Files are saved in three locations:
- **SSD**
- **Computer**
- **GitHub repository**

---

## Notes for Shay

### 1. Device Connection & Pre-settings
- **Lines 1–56**: Connects devices and sets initial parameters.

### 2. Temperature Control
- **Lines 60–80**: The experiment pauses until the temperature reaches the target.

### 3. Current, Voltage & Readings
- **Lines 81–130**:  
  - **`limiter`**: Stops the experiment if current exceeds the power supply limit.  
  - **`vinit`**: Initial voltage (set in **line 147**).  
  - **`vstep`**: Voltage step size (set in **line 148**).  

### 4. Main Experiment Control
- **Lines 132–168**:
  - **`Vinit`**: Initial voltage.  
  - **`Vstep`**: Voltage step size.  
  - **`Object_temp`**: Target measurement temperature.  
  - **`n_pts`**: Number of data points (program stops if current exceeds 0.1A).  
  - **Loop Control**:  
    - **Line 156 & Line 189** set the number of experiment repetitions.  
    - Default: `range(1,4)` (repeats 3 times per temperature).  
    - **⚠️ Change both lines together to avoid errors.**  

### 5. Email Notification (Optional)
- **Lines 170–end**: Sends collected data via email.  
- To configure:
  - **Line 174**: Replace with your email:
    ```python
    mail_receivers = ["your_email@gmail.com"]
    ```
  - **Line 180**: Replace `"sample"` and email:
    ```python
    mm['To'] = "YourName<your_email@gmail.com>"
    ```
- **To disable email notifications**, delete everything after **line 170**.  

---

## Running the Script
Navigate to the script directory in the command line and run:

```sh
python measureltVnew.py n_pts
```

- No need to specify a filename.
- The program automatically generates filenames in the format:

  ```
  TxxxVx.dat
  ```

  where:
  - `xxx` = Temperature in Kelvin  
  - `x` = Experiment sequence  

---

📖 **Open for reading and communication.**
