SpeakerMotion.Models.Campaign = Backbone.RelationalModel.extend
    defaults:
        name: ""
        code: ""
        manager: null
        reviewers: []
        speakers: []
        published: false
        archived: false

    relations: [
        {
            type: Backbone.HasOne
            key: 'manager'
            relatedModel: 'SpeakerMotion.Models.User'
        },
        {
            type: Backbone.HasMany
            key: 'reviewers'
            relatedModel: 'SpeakerMotion.Models.User'
        },
        {
            type: Backbone.HasMany
            key: 'speakers'
            relatedModel: 'SpeakerMotion.Models.User'
        },
    ]

    initialize: ->

    urlRoot: "/api/v1/campaign/"

    toJSON: ->
        id: @get 'id'
        name: @get 'name'
        code: @get 'code'
        manager: @get('manager')
        published: @get 'published'
        archived: @get 'archived'