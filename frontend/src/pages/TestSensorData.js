import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

const styles = theme => ({
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
});

class TestSensorData extends React.Component {
  state = {
    text: '',
    data: ''
  };

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
          style={{ width: 500 }}
          onChange={(ev) => {
            this.setState({ text: ev.target.value })
          }}
        />
        <br />
        <Button variant="contained" className={classes.button} onClick={() => {
          console.log(this.state.text)
          console.log(this.state.data)
          fetch('http://localhost:5000/sensor_data', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            body: this.state.text
          })
            .then((response) => {
              if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                  response.status);
                return;
              }

              // Examine the text in the response
              response.json().then((data) => {
                this.setState({ data: data.data })
              });
            }
            )
            .catch(function (err) {
              console.log('Fetch Error :-S', err);
            });
        }}>
          Send
        </Button>
        <br />
        {this.state.data}
      </div>
    );
  }
}

export default withStyles(styles)(TestSensorData);

// {
//   "deviceID": "34124412",
//   "patientID": "92152244",
//   "sensorData": {
//     "colour": {
//       "R": 12,
//       "G": 245,
//       "B": 189
//     },
//     "pH": 6.2,
//     "glucose": "5 mmol/L",
//     "protein": "0.7 g/l"
//   }
// }