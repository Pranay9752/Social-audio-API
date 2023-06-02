# Social-audio-API

This is a Django REST Framework API project that provides various endpoints for managing users, authentication, registration, songs, albums, podcasts, playlists, and social interactions. Below is a detailed explanation of each endpoint:

## Admin Endpoints

`/admin/password/reset/` - Endpoint for resetting a user's password.

`/admin/password/reset/confirm/` - Endpoint for confirming the password reset request.

`/admin/login/` - Endpoint for user login.

`/admin/logout/` - Endpoint for user logout.

`/admin/user/` - Endpoint for retrieving and updating user details.

`/admin/password/change/` - Endpoint for changing user password.

## Registration Endpoints

`/registration/account-confirm-email/(?P<key>.+)/` - Endpoint for confirming the user's email address.

`/registration/register/` - Endpoint for user registration.

## Authentication Endpoints

`/auth/login/` - Endpoint for user login.

`/auth/logout/` - Endpoint for user logout.

## User Endpoints

`/user/followers/` - Endpoint for retrieving the followers of a user.

`/user/following/` - Endpoint for retrieving the users followed by a user.

`/user/following/edit/` - Endpoint for editing the list of users followed by a user.

`/user/search/(?P<username>[\w-]+)/` - Endpoint for searching a user by username.

`/user/profile/` - Endpoint for retrieving the profile of the authenticated user.

## Song Endpoints

`/song/` - Endpoint for creating a new song.

`/songs/` - Endpoint for retrieving the list of songs created by the authenticated user.

`/songs/all/` - Endpoint for retrieving the list of all songs.

`/songs/(?P<pk>.+)/` - Endpoint for retrieving, updating, or deleting a specific song by its primary key.

## Album Endpoints

`/album/` - Endpoint for creating a new album.

`/albums/all/` - Endpoint for retrieving the list of all albums.

`/albums/` - Endpoint for retrieving the list of albums created by the authenticated user.

`/album/(?P<pk>.+)/` - Endpoint for retrieving, updating, or deleting a specific album by its primary key.

`/album/songentry/` - Endpoint for adding a song to an album.

## Podcast Endpoints

`/podcast/all/` - Endpoint for retrieving the list of all podcasts.

`/podcasts/` - Endpoint for retrieving the list of podcasts.

`/podcast/(?P<pk>.+)/` - Endpoint for retrieving a specific podcast by its primary key.

## Playlist Endpoints

`/playlists/all/` - Endpoint for retrieving the list of all playlists.

`/playlists/` - Endpoint for retrieving the list of playlists.

`/playlist/(?P<pk>.+)/` - Endpoint for retrieving a specific playlist by its primary key.

## Social Interactions Endpoints

`/(?P<user__username>[\w-]+)/followers/` - Endpoint for retrieving the followers of a specific user.

`/(?P<user__username>[\w-]+)/following/` - Endpoint for retrieving the users followed by a specific user.

## Home Endpoints

`/home/feed/` - Endpoint for retrieving the home feed.

`/pastvibes` - Endpoints to return songs you have a vibe in past

## Trending Endpoint

`/trending/` - Endpoint for retrieving the trending content.

## Stories Endpoints

`/stories/create/` - Endpoint for creating a new story.

`/(?P<user__username>[\w-]+)/stories/(?P<pk>\d+)/` - Endpoint for retrieving, updating, or deleting a specific story by its primary key
