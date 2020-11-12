let home = new Vue({
    el: "#home",
    data: function() {
        return {
            tweets: [],
        };
    },
    methods: {
        postTweet: function(e) {
            let data = new FormData(e.target);
            axios.post('post_tweet/', data)
            .then(res => {
                console.log(res);
                this.clearTweetForm();
            })
            .catch(err => console.log(err));
        },
        clearTweetForm: function() {
            let content = document.getElementById("content");
            content.value = '';
        },
    },
    mounted: function() {
        axios.defaults.headers['X-CSRFToken'] = Cookies.get('csrftoken');
    },
});