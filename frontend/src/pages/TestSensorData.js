import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const styles = theme => ({
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
});

class TestSensorData extends React.Component {
  render() {
    const { classes } = this.props;

    return (
      <div>
        <TextField
          id="standard-textarea"
          label="Input test data"
          multiline
          className={classes.textField}
          margin="normal"
          onKeyPress={(ev) => {
            console.log(`Pressed keyCode ${ev.key}`);
            if (ev.key === 'Enter') {
              fetch('http://localhost:5000/sensor_data', {
                method: 'POST',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  "deviceID": "34124412",
                  "patientID": "92152244",
                  "sensorData": {
                    "colour": {
                      "R": 12,
                      "G": 245,
                      "B": 189
                    },
                    "pH": 6.2,
                    "glucose": "5 mmol/L",
                    "protein": "0.7 g/l"
                  }
                })
              })
              .then(
                function(response) {
                  if (response.status !== 200) {
                    console.log('Looks like there was a problem. Status Code: ' +
                      response.status);
                    return;
                  }
            
                  // Examine the text in the response
                  response.json().then(function(data) {
                    console.log(data);
                  });
                }
              )
              .catch(function(err) {
                console.log('Fetch Error :-S', err);
              });
            }
          }}
        />
      </div>
    );
  }
}

export default withStyles(styles)(TestSensorData);