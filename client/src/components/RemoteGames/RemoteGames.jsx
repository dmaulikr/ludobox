import React from 'react'
import GamesTable from '../GamesTable/GamesTable.jsx'

import APIClient from "../../api.js"

export default class RemoteGames extends React.Component {

  constructor(props) {
    super(props)

    // fetch data from the local box
    this.localApi = new APIClient();

    this.state = {
      remoteGames: [],
      localGames: []
    };
  }

  fetchRemoteGames() {
    this.remoteApi.getGames(remoteGames =>  this.setState({ remoteGames }) );
  }

  fetchLocalGames() {
    this.localApi.getGames(localGames =>  this.setState({ localGames }) );
  }

  componentWillReceiveProps(nextProps) {
    console.log("nextProps",nextProps);
    if (nextProps.config && nextProps.config.config.web_server_url) {

      // connect to remote server
      this.remoteAddress = nextProps.config.config.web_server_url;
      this.remoteApi = new APIClient({ baseUrl : this.remoteAddress });

      // get all data
      this.fetchRemoteGames()
    }
  }

  componentDidMount() {
    this.fetchLocalGames()
  }

  render() {

    console.log(this.props.config);
    // // check which games already exists locally on the box
    let localGamesSlugs = this.state.localGames.map( d => d.slug)

    let games = this.state.remoteGames.map( d => {
      let existsLocally = localGamesSlugs.indexOf(d.slug) !== -1 ? true : false;
      return { ...d, existsLocally}
    })

    return (
      <div>
        <h3>Download games on this box</h3>
        {
          this.state.remoteGames.length ?
          <p>
            {`Remote server at : ${this.remoteAddress} (${this.state.remoteGames.length} games)`}
          </p>
          :
          null
        }
        {
          this.state.remoteGames.length ?
          <GamesTable
            games={games}
            remoteApi={this.remoteApi}
            localApi={this.localApi}
          />
          :
          "No additional games available, sorry."
        }
      </div>
    )
  }


}
