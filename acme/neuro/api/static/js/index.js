// Index

var Index = React.createClass({

    getInitialState: function() {
        return {
            tweets: [],
            tweets_search: '',
            searching_state: false,
        };
    },

    updateTweetsSearch: function(evt) {
        this.setState({
            tweets_search: evt.target.value
        });
    },

    fetchTweets: function() {
        this.setState({tweets: []});
        this.setState({searching_state: true});
        //
        var url = '/api/v1/tweets/?lang=ru&search=' + this.state.tweets_search;
        //
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({tweets: data.objects});
                this.setState({searching_state: false});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(url, status, err.toString());
                this.setState({searching_state: false});
            }.bind(this)
        });
    },

    render: function() {

        var tweets = this.state.tweets.map(function(tweet) {
            return (
                <tr key={tweet._id}>
                    <th>{tweet.value}</th>
                    <th>{tweet.text}</th>
                    <th>{tweet.author}</th>
                </tr>
            );
        });

        return (
            <div className='neuro-body'>
                <h1>ACME / Neuro</h1>

                <div className="row">
                    <div className="col-lg-6">
                        <div className="input-group">
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Введите слово или несколько слов для поиска"
                                onChange={this.updateTweetsSearch}
                                disabled={this.state.searching_state}
                            />

                            <span className="input-group-btn">
                                <button
                                    className="btn btn-primary"
                                    onClick={this.fetchTweets}
                                    disabled={ this.state.searching_state || ! this.state.tweets_search }
                                >
                                    Искать в twitter
                                </button>
                            </span>
                        </div>
                    </div>
                </div>

                <img
                    src="/static/images/loader.gif"
                    height='40px'
                    hidden={ ! this.state.searching_state }
                    aligin='center'
                />

                <table
                    className="table table-bordered table-striped table-responsive"
                    hidden={ ! tweets.length }
                >
                    <thead>
                        <tr>
                            <th>Оценка</th>
                            <th>Текст</th>
                            <th>Автор</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tweets}
                    </tbody>
                </table>

            </div>
        );
    }
});


// Application

var Application = React.createClass({
    render: function() {
        return (
            <div className='neuro-application container'>
                <Index />
            </div>
        );
    }
});


// Run

ReactDOM.render(
    <Application />,
    document.getElementById('application')
);
