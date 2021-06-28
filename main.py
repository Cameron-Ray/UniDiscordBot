import os
from datetime import datetime, timedelta

import discord
from dotenv import load_dotenv

import messages

load_dotenv()


def isUserAdmin(msgRoles):
    for r in msgRoles:
        if r.name == 'Admin':
            return True

    return False


class EEEBot(discord.Client):

    # Official Bot Color
    BOTCOLOR = 0x01BB22

    # Message IDs
    projectsMessageID = 0
    yearOfStudyMessageID = 0
    streamMessageID = 0

    # Channel IDs
    hobbyRequestsChannelID = int(os.getenv('hobbyRequestsChannelID'))
    newProjectsChannelID = int(os.getenv('newProjectsChannelID'))
    adminCtrlChannelID = int(os.getenv('adminCtrlChannelID'))
    welcomeChannelID = int(os.getenv('welcomeChannelID'))
    courseManagerChannelID = int(os.getenv('courseManagerChannelID'))

    # Help Messages
    helpTitle = "EEE Bot - Help"
    helpDescription = "These are the following commands you may use in this channel:\n\n"

    # Emoji IDs
    emojis = {
        "ee": "<:EE:841368870623248414>",
        "ece": "<:ECE:841368870648414248>",
        "mtrx": "<:MTRX:841368870395838547>",
        "csc": "<:CSC:841414624913391657>",
        1: "\U00000031\U000020E3",
        2: "\U00000032\U000020E3",
        3: "\U00000033\U000020E3",
        4: "\U00000034\U000020E3",
        "E": "\U0001F1EA",
        "thumbup": "\U0001f44d",
        "thumbdown": "\U0001F44E",
    }

    # Server Roles
    serverRoles = {}

    # role management
    userRoleManagement = {}

    # temp role assignment, member.id: {year: number, stream: text, elective:bool}
    tempRoleConfig = {}

    # check if user has admin role

    def addRoles(self, userID, stream, years, elective):
        self.userRoleManagement[userID] = []

        if years == None or stream == None:
            return

        # First year Role
        if 1 in years and stream != self.emojis['csc']:
            self.userRoleManagement[userID].append(
                self.serverRoles['EEE - 1st Year'])

        # Second year Roles
        if 2 in years and stream == self.emojis['csc']:
            self.userRoleManagement[userID].append(
                self.serverRoles['CSC - 2nd Year'])

        if 2 in years and stream != self.emojis['csc']:
            self.userRoleManagement[userID].append(
                self.serverRoles['EEE - 2nd Year'])

        # Third year Roles
        if 3 in years and stream == self.emojis['ece']:
            self.userRoleManagement[userID].append(
                self.serverRoles['ECE - 3rd Year'])

        if 3 in years and stream == self.emojis['ee']:
            self.userRoleManagement[userID].append(
                self.serverRoles['EE - 3rd Year'])

        if 3 in years and stream == self.emojis['mtrx']:
            self.userRoleManagement[userID].append(
                self.serverRoles['MTRX - 3rd Year'])

        if 3 in years and stream == self.emojis['csc']:
            self.userRoleManagement[userID].append(
                self.serverRoles['CSC - 3rd Year'])

        # Fourth year Role
        if 4 in years and stream == self.emojis['ece']:
            self.userRoleManagement[userID].append(
                self.serverRoles['ECE - 4th Year'])

        if 4 in years and stream == self.emojis['mtrx']:
            self.userRoleManagement[userID].append(
                self.serverRoles['MTRX - 4th Year'])

        if 4 in years and stream == self.emojis['ee']:
            self.userRoleManagement[userID].append(
                self.serverRoles['EE - 4th Year'])

        # Electives Role
        if elective:
            self.userRoleManagement[userID].append(
                self.serverRoles['Electives'])

        return

    ##################
    # On Ready Event #
    ##################

    async def on_ready(self):
        timeInstant = datetime.now() + timedelta(minutes=60)

        w = self.guilds[0].get_channel(self.newProjectsChannelID)
        await w.purge(before=timeInstant)

        newProjectsEmbed = discord.Embed(
            description=messages.newAddAproject, color=self.BOTCOLOR)
        newProjectsEmbed.set_author(name="How To Create A New Project",
                                    icon_url=self.user.avatar_url)
        await w.send(embed=newProjectsEmbed)

        w = self.guilds[0].get_channel(self.welcomeChannelID)
        await w.purge(before=timeInstant)

        newWelcomeEmbed = discord.Embed(description=messages.newWelcome,
                                        color=self.BOTCOLOR)
        newYOSEmbed = discord.Embed(description=messages.newYOS,
                                    color=self.BOTCOLOR)
        newStreamEmbed = discord.Embed(description=messages.newStream,
                                       color=self.BOTCOLOR)
        newWelcomeEmbed.set_author(name="Welcome and Rules!",
                                   icon_url=self.user.avatar_url)
        newYOSEmbed.set_author(name="Select A Year Of Study",
                               icon_url=self.user.avatar_url)
        newStreamEmbed.set_author(name="Select Your Stream",
                                  icon_url=self.user.avatar_url)

        await w.send(embed=newWelcomeEmbed)
        m2 = await w.send(embed=newYOSEmbed)
        m3 = await w.send(embed=newStreamEmbed)

        await m2.clear_reactions()
        await m2.add_reaction(self.emojis[1])
        await m2.add_reaction(self.emojis[2])
        await m2.add_reaction(self.emojis[3])
        await m2.add_reaction(self.emojis[4])
        await m2.add_reaction(self.emojis["E"])

        await m3.clear_reactions()
        await m3.add_reaction(self.emojis["ee"])
        await m3.add_reaction(self.emojis["ece"])
        await m3.add_reaction(self.emojis["mtrx"])
        await m3.add_reaction(self.emojis["csc"])

        for role in self.guilds[0].roles:
            self.serverRoles[role.name] = role

        self.yearOfStudyMessageID = m2.id
        self.streamMessageID = m3.id

        botAct = discord.CustomActivity('Listening to !EEE')
        await self.change_presence(status=discord.Status.online,
                                   activity=botAct)

        await self.guilds[0].get_channel(
            self.adminCtrlChannelID
        ).send(embed=discord.Embed(description='EEE Bot Online on ' + datetime.now().strftime("%d/%m/%Y @ %H:%M:%S"), color=self.BOTCOLOR))
        return

    ####################
    # On Message Event #
    ####################
    async def on_message(self, msg):
        if msg.author == self.user:
            return

        # get guild object
        guild = self.guilds[0]

        # get channel objects
        hobbyRequestsChannel = guild.get_channel(self.hobbyRequestsChannelID)

        # get category objects

        ######################
        # Add Course Command #
        ######################
        if msg.content.startswith('!EEE AddCourse ') and (
                msg.channel.id == self.adminCtrlChannelID
                or msg.channel.id == self.courseManagerChannelID):
            courseDetails = msg.content.split('!EEE AddCourse ')[1]
            courseDetails = courseDetails.split(' ')

            if len(courseDetails) == 4:
                courseCode = courseDetails[0]
                year = int(courseDetails[1])
                stream = courseDetails[2]
                elective = courseDetails[3]
            else:
                await msg.channel.send(
                    'That command is invalid, please try again!')
                return

            yearCategory = guild.categories[year + 3]

            textCreated = await guild.create_text_channel(
                courseCode, category=yearCategory)
            voiceCreated = await guild.create_voice_channel(
                courseCode + '-voice', category=yearCategory)

            if textCreated != None and voiceCreated != None:
                await msg.channel.send('Created Course Channels for ' +
                                       courseCode)
            else:
                await hobbyRequestsChannel.send(
                    'Unable to create course channels for ' + courseCode)
            return

        #######################
        # Add Project Command #
        #######################
        if msg.content.startswith(
                '!EEE AddProject '
        ) and msg.channel.id == self.newProjectsChannelID and msg.channel.category == self.guilds[0].categories[9]:
            cmdContent = msg.content.split('!EEE AddProject ')[1]
            newProjectName = cmdContent[0:cmdContent.find(' ')]
            projectDescription = cmdContent.split(newProjectName + ' ')[1]
            projectDescription = projectDescription[1:len(projectDescription) -
                                                    1]

            approvalMessage = await hobbyRequestsChannel.send(
                'Approval needed for new project: \n\n |' + newProjectName +
                '|\n\n' + projectDescription)
            await approvalMessage.add_reaction(self.emojis['thumbup'])
            await approvalMessage.add_reaction(self.emojis['thumbdown'])
            await msg.channel.send(embed=discord.Embed(description='Your request to create ' + newProjectName +
                                   ' has been successfully submitted!'))
            return

        ##########################
        # Delete Project Command #
        ##########################
        if msg.content.startswith('!EEE DeleteThisProject ') and msg.channel.category == self.guilds[0].categories[9] and msg.channel.id != self.newProjectsChannelID:
            deleteReason = msg.content.split('!EEE DeleteThisProject ')[1]
            if deleteReason != '':
                vcName = msg.channel.name + '-voice'

                for vc in msg.channel.category.voice_channels:
                    if vc.name == vcName:
                        await vc.delete(reason=deleteReason)
                        await msg.channel.delete(reason=deleteReason)
            else:
                await msg.channel.send(embed=discord.Embed(description='Please provide a valid description for the deletion!'))

            return

        #########################
        # Clear Channel Command #
        #########################
        if msg.content.startswith('!EEE clearChannel') and isUserAdmin(
                msg.author.roles):
            timeInstant = datetime.now() + timedelta(seconds=60)

            def is_not_Announcement(m):
                return m.id != self.projectsMessageID

            await msg.channel.purge(before=timeInstant,
                                    check=is_not_Announcement)
            return

        ################
        # Help Command #
        ################
        # or msg.content.startswith('!EEE help') or msg.content.startswith('!EEE HELP'):
        if msg.content.upper().startswith('!EEE HELP'):
            helpEmbed = discord.Embed(title="EEE Bot - Help Menu",
                                      description="Coming Soon!")
            await msg.channel.send(embed=helpEmbed)
            return

        ###################
        # Invalid Command #
        ###################
        if msg.content.startswith('!EEE') or msg.content.startswith('!EE') or msg.content.startswith('!E') or msg.content.startswith('!'):
            await msg.channel.send(embed=discord.Embed(description='''Sorry, that command isn\'t correct, available or you don\'t have the permissions to use it here!

            Please make sure that you use the command prefix "!EEE" and the relevant command. Type "!EEE help" for some more hlp on this.'''))
            return

    ######################
    # Reaction Add Event #
    ######################
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id:
            return

        # fetch guild
        guild = self.guilds[0]

        ##############################
        # New Hobby Reaction Manager #
        ##############################
        if payload.channel_id == self.hobbyRequestsChannelID:

            # fetch channels
            hobbyRequestsChannel = self.get_channel(
                self.hobbyRequestsChannelID)
            newProjectsChannel = self.get_channel(self.newProjectsChannelID)

            if payload.emoji.name == '👍':
                newApprovalMsg = await hobbyRequestsChannel.fetch_message(payload.message_id)
                approvalMsg = newApprovalMsg.content
                newProjectName = approvalMsg[approvalMsg.find('|') + 1:]
                newProjectName = newProjectName[:newProjectName.find('|')]

                hobbyCategory = guild.categories[9]
                textCreated = await guild.create_text_channel(
                    newProjectName, category=hobbyCategory)
                voiceCreated = await guild.create_voice_channel(
                    newProjectName + '-voice', category=hobbyCategory)

                if textCreated != None and voiceCreated != None:
                    projectCreatedEmbed = discord.Embed(
                        description=messages.deleteAProject, color=self.BOTCOLOR)
                    projectCreatedEmbed.set_author(name="Congrats on creating your new project: " + newProjectName,
                                                   icon_url=self.user.avatar_url)
                    await textCreated.send(embed=projectCreatedEmbed)
                    await newProjectsChannel.send(embed=discord.Embed(description='Your project, ***' + newProjectName +
                                                                      '***, was approved!\n\nYou can now use the text and voice channel related to this.'
                                                                      )
                                                  )

                    await newApprovalMsg.delete()
                else:
                    await hobbyRequestsChannel.send(embed=discord.Embed(description='The action you attempeted was unsuccessful'))

            if payload.emoji.name == '👎':
                approvalMsg = await hobbyRequestsChannel.fetch_message(
                    payload.message_id)
                await approvalMsg.delete()

                approvalMsg = approvalMsg.content
                newProjectName = approvalMsg[approvalMsg.find('|') + 1:]
                newProjectName = newProjectName[:newProjectName.find('|')]
                await newProjectsChannel.send(embed=discord.Embed(description='Unfortunately your project, ***' + newProjectName +
                                                                  '***, was not approved!'))

        #########################
        # Role Reaction Manager #
        #########################
        if payload.channel_id == self.welcomeChannelID:
            ch = guild.get_channel(self.welcomeChannelID)
            m = await ch.fetch_message(payload.message_id)

            if not str(payload.emoji) in self.emojis.values():
                await m.remove_reaction(payload.emoji, payload.member)
                return

            if not payload.user_id in self.tempRoleConfig:
                self.tempRoleConfig[payload.user_id] = {
                    'years': [],
                    'stream': None,
                    'elective': False
                }

            # Set Year of study role
            if payload.message_id == self.yearOfStudyMessageID:
                if payload.emoji.name == self.emojis[1]:
                    self.tempRoleConfig[payload.user_id]['years'].append(1)
                if payload.emoji.name == self.emojis[2]:
                    self.tempRoleConfig[payload.user_id]['years'].append(2)
                if payload.emoji.name == self.emojis[3]:
                    self.tempRoleConfig[payload.user_id]['years'].append(3)
                if payload.emoji.name == self.emojis[4]:
                    self.tempRoleConfig[payload.user_id]['years'].append(4)
                if payload.emoji.name == self.emojis['E']:
                    self.tempRoleConfig[payload.user_id]['elective'] = True

            if payload.message_id == self.streamMessageID:
                oldStream = self.tempRoleConfig[payload.user_id]['stream']

                if oldStream != None:
                    if str(payload.emoji) != self.emojis['ece']:
                        await m.remove_reaction(self.emojis['ece'],
                                                payload.member)
                    if str(payload.emoji) != self.emojis['ee']:
                        await m.remove_reaction(self.emojis['ee'],
                                                payload.member)
                    if str(payload.emoji) != self.emojis['mtrx']:
                        await m.remove_reaction(self.emojis['mtrx'],
                                                payload.member)
                    if str(payload.emoji) != self.emojis['csc']:
                        await m.remove_reaction(self.emojis['csc'],
                                                payload.member)

                hasUserReacted = False

                for react in m.reactions:
                    users = await react.users().flatten()
                    for user in users:
                        if user.id == payload.user_id:
                            hasUserReacted = True

                if not hasUserReacted:
                    self.tempRoleConfig[payload.user_id]['stream'] = None
                else:
                    self.tempRoleConfig[payload.user_id]['stream'] = str(
                        payload.emoji)

            stream = self.tempRoleConfig[payload.user_id]['stream']
            years = self.tempRoleConfig[payload.user_id]['years']
            elective = self.tempRoleConfig[payload.user_id]['elective']

            for role in payload.member.roles:
                if role.name != '@everyone':
                    await payload.member.remove_roles(role)

            if stream != None and years != None:
                self.addRoles(payload.user_id, stream, years, elective)
                for role in self.userRoleManagement[payload.user_id]:
                    await payload.member.add_roles(role)

    #########################
    # Reaction Remove Event #
    #########################

    async def on_raw_reaction_remove(self, payload):
        guild = self.guilds[0]
        actionMember = await guild.fetch_member(payload.user_id)

        if payload.user_id == self.user.id:
            return

        #########################
        # Role Reaction Manager #
        #########################
        if payload.channel_id == self.welcomeChannelID:
            # Set Year of study role
            if payload.message_id == self.yearOfStudyMessageID:
                if payload.emoji.name == self.emojis[1]:
                    self.tempRoleConfig[payload.user_id]['years'].remove(1)
                if payload.emoji.name == self.emojis[2]:
                    self.tempRoleConfig[payload.user_id]['years'].remove(2)
                if payload.emoji.name == self.emojis[3]:
                    self.tempRoleConfig[payload.user_id]['years'].remove(3)
                if payload.emoji.name == self.emojis[4]:
                    self.tempRoleConfig[payload.user_id]['years'].remove(4)
                if payload.emoji.name == self.emojis['E']:
                    self.tempRoleConfig[payload.user_id]['elective'] = False
                if self.tempRoleConfig[payload.user_id]['years'] == []:
                    self.tempRoleConfig[payload.user_id]['years'] = None

            if payload.message_id == self.streamMessageID:
                self.tempRoleConfig[payload.user_id]['stream'] = None

            stream = self.tempRoleConfig[payload.user_id]['stream']
            years = self.tempRoleConfig[payload.user_id]['years']

            for role in actionMember.roles:
                if role.name != '@everyone':
                    await actionMember.remove_roles(role)

            self.addRoles(payload.user_id, stream, years,
                          self.tempRoleConfig[payload.user_id]['elective'])

            if stream != None and years != None:
                for role in self.userRoleManagement[payload.user_id]:
                    await actionMember.add_roles(role)


##############
# Client run #
##############
client = EEEBot()
client.run(os.getenv('TOKEN'))
