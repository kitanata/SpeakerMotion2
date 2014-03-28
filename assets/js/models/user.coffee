SpeakerMotion.Models.User = Backbone.Model.extend
    defaults:
        full_name: ""

    initialize: ->

    urlRoot: "/api/v1/user/"
