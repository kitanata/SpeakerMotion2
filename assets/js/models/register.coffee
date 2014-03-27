SpeakerMotion.Models.Register = Backbone.Model.extend
    defaults:
        email: ""
        full_name: ""
        password: ""
        confirm: ""

    initialize: ->

    urlRoot: "/register"

    validation:
        email:
            required: true
            pattern: 'email'
            msg: "A valid email is required to register."
        full_name:
            required: true
            msg: "Your name is required to register."
        password:
            required: true
            minLength: 8
            msg: "A password that is at least 8 characters long is required."
        confirm:
            required: true
            equalTo: 'password'
            msg: "Your passwords do not match."
