import * as React from 'react';
import PropTypes from 'prop-types';
import List from '@mui/material/List';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import Paper from '@mui/material/Paper';
import ListItemText from '@mui/material/ListItemText';
import {
  Link as RouterLink,
  MemoryRouter,
} from 'react-router-dom';

function Router(props) {
  const { children } = props;

  return (
    <MemoryRouter initialEntries={['/drafts']} initialIndex={0}>
      {children}
    </MemoryRouter>
  );
}

Router.propTypes = {
  children: PropTypes.node,
};

function ListItemLink(props) {
  const { primary, to } = props;

  const renderLink = React.useMemo(
    () =>
      React.forwardRef(function Link(itemProps, ref) {
        return <RouterLink to={to} ref={ref} {...itemProps} role={undefined} />;
      }),
    [to],
  );

  return (
    <li>
      <ListItem button component={renderLink}>
        <ListItemText primary={primary} />
      </ListItem>
    </li>
  );
}

ListItemLink.propTypes = {
  icon: PropTypes.element,
  primary: PropTypes.string.isRequired,
  to: PropTypes.string.isRequired,
};

export default function ListRouter() {
  return (
    <div>
      <Box sx={{ width: "inherit" }}>
        <Paper elevation={0}>
          <List aria-label="secondary mailbox folders">
            <ListItemLink to="/app/map" primary="Map" />
            <ListItemLink to="/app/face" primary="Face" />
            {/* <ListItemLink to="/app/voice" primary="Voice" /> */}
          </List>
        </Paper>
      </Box>
    </div>
  );
}