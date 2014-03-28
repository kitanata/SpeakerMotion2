SpeakerMotion.Models.User = Backbone.RelationalModel.extend
    defaults:
        full_name: ""

    urlRoot: "/api/v1/user"

    toJSON: ->
        full_name: @get('full_name')
