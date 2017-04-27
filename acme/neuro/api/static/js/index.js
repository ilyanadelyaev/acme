// Index

var Index = React.createClass({

    getInitialState: function() {
        return {
            tweets: [],
            tweets_search: '',
            button_disabled: false,
            input_disabled: false,
        };
    },

    updateTweetsSearch: function(evt) {
        this.setState({
            tweets_search: evt.target.value
        });
    },

    fetchTweets: function() {
        this.setState({
            button_disabled: true,
            input_disabled: true
        });
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
                this.setState({
                    button_disabled: false,
                    input_disabled: false
                });
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(url, status, err.toString());
                this.setState({
                    button_disabled: false,
                    input_disabled: false
                });
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

                <input
                    type="text"
                    onChange={this.updateTweetsSearch}
                    disabled={this.state.input_disabled}
                />

                <button
                    className="btn btn-primary"
                    onClick={this.fetchTweets}
                    disabled={this.state.button_disabled}
                >
                    Fetch tweets
                </button>

                <table className="table table-bordered table-striped table-responsive">
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
