import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import FormGroup from '@material-ui/core/FormGroup';
import Switch from '@material-ui/core/Switch';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';


export default function TransactionTypeSwitch(props) {

  return (
    <FormGroup>
      <Typography component="div">
        <Grid component="label" container alignItems="center" spacing={1}>
          <Grid item>Income</Grid>
          <Grid item>
            <AntSwitch
              checked={props.selections.selectExpenses}
              onChange={props.handleChange}
              name="selectExpenses" />
          </Grid>
          <Grid item>Expenses</Grid>
        </Grid>
      </Typography>
    </FormGroup>
  );
}


const AntSwitch = withStyles((theme) => ({
  root: {
    width: 28,
    height: 16,
    padding: 0,
    display: 'flex',
  },
  switchBase: {
    padding: 2,
    color: theme.palette.common.white,
    '&$checked': {
      transform: 'translateX(12px)',
      color: theme.palette.common.white,
      '& + $track': {
        opacity: 1,
        backgroundColor: theme.palette.error.light,
        borderColor: theme.palette.error.light,
      },
    },
  },
  thumb: {
    width: 12,
    height: 12,
    boxShadow: 'none',
  },
  track: {
    border: `1px solid ${theme.palette.grey[500]}`,
    borderRadius: 16 / 2,
    opacity: 1,
    backgroundColor: theme.palette.success.light,
    borderColor: theme.palette.success.light,
  },
  checked: {},
}))(Switch);
