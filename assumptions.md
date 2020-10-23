# COMP1531 Major Project Assumptions

## AUTH.PY

* Logging in is determined by whether or not the user's token is set as their email
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


## CHANNEL.PY

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


## CHANNELS.PY

* The listall feature does not require any authentication
* Channel names can consist of any characters
    * However, channel names cannot exceed 20 characters in length
* Channel names are allowed to be identical to other channel names
* The creator of a channel is automatically assigned as the sole owner of the channel
* All channel owners are also considered channel members

## MESSAGE.PY

* An empty message cannot be added to a channel
* When editing a message, details such as time_created and u_id will not be modified even if another user is editing it
* Users cannot edit/delete their own messages unless they are an owner (or FlockR owner)
* You must be a channel owner (or FlockR owner) to edit/delete messages
* A message cannot be deleted/edited if it was created by a channel owner (or FlockR owner)

## USER.PY

> TODO

## OTHER.PY

> TODO

## OTHER ASSUMPTIONS

* The user and channel data is stored in data.py
    * They are both arrays inside a larger dictionary
    * The data of each user and channel is stored in separate dictionaries
* If the FlockR owner leaves the system, then the next registered user is the new FlockR owner
    * They are informed of this the next time they log in