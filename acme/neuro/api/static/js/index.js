// Index

var Index = React.createClass({

    render: function() {
        return (
            <div className='neuro-body'>
                <h1>ACME / Neuro</h1>
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
