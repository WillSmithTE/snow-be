const fetch = require('node-fetch');

exports.handler = async () => {
    const endpoint = 'https://ski-be-hgfltltt5a-de.a.run.app/api/refreshData'
    return fetch(endpoint, {method: 'POST'});
};
