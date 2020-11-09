# COMP1531 Major Project Assumptions

## AUTH.PY

* Logging in is determined by whether or not the user's token is set
    * If it is not set, then they cannot log in
* The user is informed if the email is registered but the password does not match the email
    * The program returns a message which indicates that the entered password is incorrect
* Logging out sets the user's token to an empty string
* Logging out uses the user's token
    * If the token is not recognised, the program assumes that the user is not registered
    * The user is informed of this
* If logging out is successful, the user is informed
    * The program assumes that they are already logged out if the token used for logging out does not exist
* The u_id is iterative:
    * The first registered user (FlockR owner), is set to user 1
    * The next user is set to user 2 and so on...
* Passwords are encoded and hashed using `hashlib` for better security
* Generated tokens are also hashed using `hashlib` and these are based on the user's email


## CHANNEL.PY

* When adding data to a channel, only the user's u_id is stored
    * `channel_details` returns the name's of each member directly from the user storage
* If the user already exists in a channel, they cannot be invited
    * This also means that you cannot invite yourself
* A user cannot join a private channel unless they are the FlockR owner
    * The only way for them to enter a private channel is to be invited by an owner of that channel
* An owner is not allowed to remove themselves
* For the FlockR owner to have channel permissions, then they must be a part of that channel
    * This means that they don't have to be a channel owner to do so
* A channel without a channel owner cannot exist (FlockR owner excepted - see below)
* The Flockr owner has the right to remove any owner
    * If the Flockr owner removes the last owner of a channel, then they automatically become a channel owner
* A negative start value in `channel_messages` defualts to 0
* `channel_messages` updates the current user's reacted messages, so that the like button is filled in on the frontend


## CHANNELS.PY

* The listall feature does not require any authentication
* Channel names can consist of any characters
    * However, channel names cannot exceed 20 characters in length
* Channel names are allowed to be identical to other channel names
* The creator of a channel is automatically assigned as the sole owner of the channel
* All channel owners are also considered channel members
* Features that require returning details of channels do not return member names
    * Only their u_id's are returned


## MESSAGE.PY

* An empty message cannot be added to a channel
    * Editing a message with an empty string deletes the message
* When editing a message, details such as time_created and u_id will not be modified even if another user is editing it
* The message_id is unique across all channels
    * It is based on the fact that there cannot be 10,000 messages in a channel
* Users cannot edit/delete their own messages unless they are an owner (or FlockR owner)
* You must be a channel owner (or FlockR owner) to edit/delete messages
    * However, they are not permitted to edit/delete other owner's messages
* Any user in the channel can react to their own message
* Multiple messages can be pinned to the same channel
* The only react type available is 'liking' a message


## USER.PY

* Users must be logged in with a valid token to change their first or last name
* Handles are unique, a user cannot set their handle to one already in use
* When uploading a photo, the extension can be any of the following:
    * .jpg
    * .jpeg
    * .JPG
    * .JPEG
* The image is saved locally inside /src/static before getting hosted on the server
    * If the static directory does not exist, it gets created
* The saved image's filename becomes a 10 character combination of random uppercase letters and digits
* The image url will be updated in the upload_url field on the frontend
* An example of the generated url is the following:
    * localhost:46472/static/HEN46S3H2K.jpg


## OTHER.PY

* Search based on query_str returns the data for all messages which contain that string
    * The cases of both the query string and the message in channel does not matter
    * e.g. query_str = 'meSsAGe' will return the data for a message with string = '1MESSAGE2'
* Query strings must contain at least 2 characters
* Owner permissions are stored seperately in user dictionaries
* There must always be a flockr owner so that last flockr owner cannot set their own permission as a member
* Setting a redundant permission will throw an error
    * e.g. Setting a member's permission to 'member'

## OTHER ASSUMPTIONS

* The user and channel data is stored in data.py
    * They are both arrays inside a larger dictionary
    * The data of each user and channel is stored in separate dictionaries
* If the FlockR owner leaves the system, then the next registered user is the new FlockR owner
    * They are informed of this the next time they log in