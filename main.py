import asyncio
import os
import sys
from datetime import datetime, timedelta

import discord
from discord import embeds
from dotenv import load_dotenv

import helpMessages as helpmsg
import otherMessages as otherMsg
import setupMessages as messages

load_dotenv()

# async handler config for windows due to
# exception produced on client.close()
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = discord.Intents.default()
intents.members = True


# helper function to check if
# supplied roles contains Admin role
def isUserAdmin(msgRoles):
    for r in msgRoles:
        if r.name == 'Admin':
            return True

    return False


# main bot class containing all functions and command events
class UniDiscordBot(discord.Client):

    if not os.path.isfile('./.env'):
        print('Please create a .env file with the relevant channel IDs first.')
        exit()

    # Bot Prefix. Adjust this to use a different prefix in your server
    BOTPREFIX = '!EEE'

    # Official Bot Color in Hex
    BOTCOLOR = 0x01BB22

    # Message IDs
    rulesMessageID = 0
    yearOfStudyMessageID = 0
    streamMessageID = 0

    # Channel IDs
    hobbyRequestsChannelID = int(os.getenv('hobbyRequestsChannelID'))
    newProjectsChannelID = int(os.getenv('newProjectsChannelID'))
    adminCtrlChannelID = int(os.getenv('adminCtrlChannelID'))
    welcomeChannelID = int(os.getenv('welcomeChannelID'))
    courseManagerChannelID = int(os.getenv('courseManagerChannelID'))
    diagnosticsChannelID = int(os.getenv('diagnosticsChannelID'))

    # Setup-Message Objects
    yearOfStudyMessage = None
    streamMessage = None

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

        # Electives Role
        if elective:
            self.userRoleManagement[userID].append(
                self.serverRoles['Electives'])

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
        return

    def configureChannelRoles(self, streams, year):
        perms = {
            self.serverRoles['EEE - 1st Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['CSC - 2nd Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['EEE - 2nd Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['CSC - 3rd Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['MTRX - 3rd Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['ECE - 3rd Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['EE - 3rd Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['MTRX - 4th Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['ECE - 4th Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['EE - 4th Year']: discord.PermissionOverwrite(view_channel=False),
            self.serverRoles['@everyone']: discord.PermissionOverwrite(view_channel=False),
        }

        # First year Role
        if year == 1:
            if ('ee' in streams) or ('ece' in streams) or ('mtrx' in streams):
                perms[self.serverRoles['EEE - 1st Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

        # Second year Roles
        if year == 2:
            if 'csc' in streams:
                perms[self.serverRoles['CSC - 2nd Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

            if ('ee' in streams) or ('ece' in streams) or ('mtrx' in streams):
                perms[self.serverRoles['EEE - 2nd Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

        # Third year Roles
        if year == 3:
            if 'ece' in streams:
                perms[self.serverRoles['ECE - 3rd Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

            if 'ee' in streams:
                perms[self.serverRoles['EE - 3rd Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

            if 'mtrx' in streams:
                perms[self.serverRoles['MTRX - 3rd Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

            if 'csc' in streams:
                perms[self.serverRoles['CSC - 3rd Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

        # Fourth year Role
        if year == 4:
            if 'ece' in streams:
                perms[self.serverRoles['ECE - 4th Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

            if 'mtrx' in streams:
                perms[self.serverRoles['MTRX - 4th Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

            if 'ee' in streams:
                perms[self.serverRoles['EE - 4th Year']
                      ] = discord.PermissionOverwrite(view_channel=True)

        return perms

    ##################
    # On Ready Event #
    ##################

    async def on_ready(self):
        # get bot's guild
        guild = self.guilds[0]

        welcomeChan = guild.get_channel(self.welcomeChannelID)

        m2 = None
        m3 = None

        async for m in welcomeChan.history(oldest_first=True):
            if m.embeds[0].author.name == 'Select A Year Of Study':
                m2 = m
            if m.embeds[0].author.name == 'Select Your Stream':
                m3 = m
            if m.embeds[0].author.name == 'Bot Offline':
                await m.delete()

        if m2 == None and m3 == None:
            print('There is a problem with the welcome messages')
        else:
            await m2.clear_reactions()
            await m3.clear_reactions()
            await m2.add_reaction(self.emojis[1])
            await m2.add_reaction(self.emojis[2])
            await m2.add_reaction(self.emojis[3])
            await m2.add_reaction(self.emojis[4])
            await m2.add_reaction(self.emojis["E"])
            await m3.add_reaction(self.emojis["ee"])
            await m3.add_reaction(self.emojis["ece"])
            await m3.add_reaction(self.emojis["mtrx"])
            await m3.add_reaction(self.emojis["csc"])

            # save msg IDs of newly generated messages
            self.yearOfStudyMessageID = m2.id
            self.streamMessageID = m3.id

            # save msg objects of newly generated messages
            self.yearOfStudyMessage = m2
            self.streamMessage = m3

        # obtain server roles and store in dict
            # formatting of dict -> 'role name': roleObject
            for role in guild.roles:
                self.serverRoles[role.name] = role
        # set custom bot presence to show bot command
        botAct = discord.Activity(
            name='!EEE', type=discord.ActivityType.listening)
        await self.change_presence(status=discord.Status.online,
                                   activity=botAct)

        # notify admin channel that bot is online
        await guild.get_channel(
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

        ########################
        # Bot Shutdown Command #
        ########################
        if msg.content.startswith(self.BOTPREFIX + ' SHUTDOWN') and msg.channel.id == self.adminCtrlChannelID and isUserAdmin(msg.author.roles):
            await msg.channel.send(embed=discord.Embed(
                description='EEE Bot has switched to offline successfully!'))
            offlineEmbed = discord.Embed(
                description=otherMsg.maintenanceOffline)
            offlineEmbed.set_author(name='Bot Offline')
            await self.yearOfStudyMessage.channel.send(embed=offlineEmbed)
            await self.yearOfStudyMessage.clear_reactions()
            await self.streamMessage.clear_reactions()
            await self.close()
            return

        #######################
        # Role Report Command #
        #######################
        if msg.content.startswith(self.BOTPREFIX + ' ROLEREPORT') and msg.channel.id == self.adminCtrlChannelID and isUserAdmin(msg.author.roles):
            report = ''

            async def sendReport(r, c, vt):
                reportEmbed = discord.Embed(
                    description=r)
                reportEmbed.set_author(name=c + ' - ' + vt)
                await msg.channel.send(embed=reportEmbed)

            for cat in guild.categories:
                report = "***" + cat.name + " category***"
                for tch in cat.text_channels:
                    report = report + tch.name + " overwrites:\n" + \
                        str(tch.overwrites) + "\n\n"
                
                await sendReport(report, cat.name, 'Text Channel Overwrites')

                report = "***" + cat.name + " category***"
                for vch in cat.voice_channels:
                    report = report + vch.name + " overwrites:\n" + \
                        str(vch.overwrites) + "\n\n"

                await sendReport(report, cat.name, 'Voice Channel Overwrites')

            return

        ######################
        # Add Course Command #
        ######################
        if msg.content.startswith(self.BOTPREFIX + ' AddCourse ') and (
                msg.channel.id == self.adminCtrlChannelID
                or msg.channel.id == self.courseManagerChannelID):
            courseDetails = msg.content.split(
                self.BOTPREFIX + ' AddCourse ')[1]
            courseDetails = courseDetails.split(' ')

            if len(courseDetails) == 4:
                courseCode = courseDetails[0]
                try:
                    year = int(courseDetails[1])
                    streams = [strm.lower()
                               for strm in courseDetails[2].split(',')]
                    elective = courseDetails[3].lower()
                except:
                    await msg.channel.send(embed=discord.Embed(description='That command is invalid, please try again!'))
                    return
                if len(streams) < 1:
                    await msg.channel.send(embed=discord.Embed(description='That command is invalid, please try again!'))
                    return

            else:
                await msg.channel.send(embed=discord.Embed(description='That command is invalid, please try again!'))
                return

            if elective == 'n':
                cat = guild.categories[year + 2]
                owrites = self.configureChannelRoles(streams, year)
            else:
                cat = guild.categories[7]
                owrites = None

            for coursechan in cat.text_channels:
                if coursechan.name == courseCode:
                    await msg.channel.send(embed=discord.Embed(description='A course with this name already exists! Delete the existing course and try again.'))
                    return

            textCreated = await guild.create_text_channel(
                courseCode, category=cat, overwrites=owrites)
            voiceCreated = await guild.create_voice_channel(
                courseCode + '-voice', category=cat, overwrites=owrites)

            if textCreated != None and voiceCreated != None:
                await msg.channel.send(embed=discord.Embed(description='Created course channels for ' +
                                       courseCode))
            else:
                await hobbyRequestsChannel.send(
                    'Unable to create course channels for ' + courseCode)

            return

        ##########################
        # Delete Course Command #
        ##########################
        if msg.content.startswith(self.BOTPREFIX + ' DeleteCourse ') and (
                msg.channel.id == self.adminCtrlChannelID
                or msg.channel.id == self.courseManagerChannelID):

            cmdContent = msg.content.split(self.BOTPREFIX + ' DeleteCourse ')
            courseToDelete = cmdContent[1].split(' ')[0]
            try:
                yearToDelete = int(cmdContent[1].split(' ')[1])
            except:
                await msg.channel.send(embed=discord.Embed(description='That command is invalid, please try again!'))
                return

            if courseToDelete != '':
                tcName = courseToDelete
                vcName = courseToDelete + '-voice'

                yearList = {
                    1: guild.categories[3],
                    2: guild.categories[4],
                    3: guild.categories[5],
                    4: guild.categories[6]
                }

                vcResult = False
                tcResult = False

                for vc in yearList[yearToDelete].voice_channels:
                    if vc.name == vcName:
                        await vc.delete(reason='Admin deleted this channel manually')
                        vcResult = True

                for tc in yearList[yearToDelete].text_channels:
                    if tc.name == tcName:
                        await tc.delete(reason='Admin deleted this channel manually')
                        tcResult = True

                if not tcResult or not vcResult:
                    await msg.channel.send(embed=discord.Embed(description='The specified course could not be found'))
                    return
                else:
                    await msg.channel.send(embed=discord.Embed(description=courseToDelete.upper() + ' was deleted successfully!'))
                    return
            else:
                await msg.channel.send(embed=discord.Embed(description='Please provide a valid description for the deletion!'))

            return

        ##########################
        # Archive Course Command #
        ##########################
        if msg.content.startswith(self.BOTPREFIX + ' ArchiveCourse ') and (
                msg.channel.id == self.adminCtrlChannelID
                or msg.channel.id == self.courseManagerChannelID):

            cmdContent = msg.content.split(self.BOTPREFIX + ' ArchiveCourse ')
            courseToArchive = cmdContent[1].split(' ')[0]
            try:
                yearToArchive = int(cmdContent[1].split(' ')[1])
            except:
                await msg.channel.send(embed=discord.Embed(description='That command is invalid, please try again!'))
                return

            if courseToArchive != '':
                tcName = courseToArchive
                vcName = courseToArchive + '-voice'

                yearList = {
                    1: guild.categories[3],
                    2: guild.categories[4],
                    3: guild.categories[5],
                    4: guild.categories[6]
                }

                vcResult = False
                tcResult = False

                for vc in yearList[yearToArchive].voice_channels:
                    if vc.name == vcName:
                        await vc.delete(reason='Admin archived this channel manually')
                        vcResult = True

                for tc in yearList[yearToArchive].text_channels:
                    if tc.name == tcName:
                        await tc.edit(
                            category=guild.categories[len(guild.categories)-2], sync_permissions=True)
                        tcResult = True

                if not tcResult or not vcResult:
                    await msg.channel.send(embed=discord.Embed(description='The specified course could not be found'))
                    return
            else:
                await msg.channel.send(embed=discord.Embed(description='Please provide a valid description for the archival!'))

            return

        #######################
        # Add Project Command #
        #######################
        if msg.content.startswith(
                self.BOTPREFIX + ' AddProject '
        ) and msg.channel.id == self.newProjectsChannelID and msg.channel.category == guild.categories[9]:
            cmdContent = msg.content.split(self.BOTPREFIX + ' AddProject ')[1]
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
        if msg.content.startswith(self.BOTPREFIX + ' DeleteThisProject ') and msg.channel.category == guild.categories[9] and msg.channel.id != self.newProjectsChannelID:
            deleteReason = msg.content.split(
                self.BOTPREFIX + ' DeleteThisProject ')[1]
            if deleteReason != '':
                vcName = msg.channel.name + '-voice'

                result = False

                for vc in msg.channel.category.voice_channels:
                    if vc.name == vcName:
                        await vc.delete(reason=deleteReason)
                        await msg.channel.delete(reason=deleteReason)
                        result = True

                if not result:
                    await msg.channel.send(embed=discord.Embed(description='The specified project could not be found'))
                    return
            else:
                await msg.channel.send(embed=discord.Embed(description='Please provide a valid description for the deletion!'))

            return

        ###########################
        # Archive Project Command #
        ###########################
        if msg.content.startswith(self.BOTPREFIX + ' ArchiveThisProject ') and msg.channel.category == guild.categories[9] and msg.channel.id != self.newProjectsChannelID:
            archiveReason = msg.content.split(
                self.BOTPREFIX + ' ArchiveThisProject ')[1]

            if archiveReason != '':
                vcName = msg.channel.name + '-voice'

                result = False

                for vc in msg.channel.category.voice_channels:
                    if vc.name == vcName:
                        await vc.delete(reason=archiveReason)
                        await msg.channel.edit(category=guild.categories[len(
                            guild.categories)-1], sync_permissions=True)
                        result = True

                if not result:
                    await msg.channel.send(embed=discord.Embed(description='The specified project could not be found'))
                    return
            else:
                await msg.channel.send(embed=discord.Embed(description='Please provide a valid description for the archival!'))

            return

        ##################################
        # Clear Project Requests Command #
        ##################################
        if msg.content.startswith(self.BOTPREFIX + ' ClearProjectRequests') and isUserAdmin(
                msg.author.roles) and (msg.channel.id == self.newProjectsChannelID):
            timeInstant = datetime.now() + timedelta(seconds=60)

            await msg.channel.purge(before=timeInstant)

            newProjectsEmbed = discord.Embed(
                description=messages.newAddAproject, color=self.BOTCOLOR)
            newProjectsEmbed.set_author(name="How To Create A New Project",
                                        icon_url=self.user.avatar_url)
            await msg.channel.send(embed=newProjectsEmbed)

            return

        ################################
        # Clear Course Manager Command #
        ################################
        if msg.content.startswith(self.BOTPREFIX + ' ClearCourseManager') and isUserAdmin(
                msg.author.roles) and (msg.channel.id == self.courseManagerChannelID):
            timeInstant = datetime.now() + timedelta(seconds=60)

            await msg.channel.purge(before=timeInstant)

            newCourseEmbed = discord.Embed(
                description=messages.courseManagement, color=self.BOTCOLOR)
            newCourseEmbed.set_author(name="How To Manage Courses",
                                      icon_url=self.user.avatar_url)
            await msg.channel.send(embed=newCourseEmbed)

            return

        #######################
        # Clear Music Command #
        #######################
        if msg.content.startswith(self.BOTPREFIX + ' ClearMusic') and msg.channel.category == guild.categories[10]:
            timeInstant = datetime.now() + timedelta(seconds=60)

            def is_not_Announcement(m):
                return (m.id != self.rulesMessageID and m.id != self.yearOfStudyMessageID and m.id != self.streamMessageID)

            await msg.channel.purge(before=timeInstant,
                                    check=is_not_Announcement)

            musicSetupEmbed = discord.Embed(
                description=messages.musicHelp, color=self.BOTCOLOR)
            musicSetupEmbed.set_author(name="How To Control The Music Bots",
                                       icon_url=self.user.avatar_url)
            await msg.channel.send(embed=musicSetupEmbed)

            return

        #########################
        # Clear Channel Command #
        #########################
        if msg.content.startswith(self.BOTPREFIX + ' ClearChannel') and isUserAdmin(
                msg.author.roles) and (msg.channel.id != self.courseManagerChannelID) and (msg.channel.id != self.newProjectsChannelID) and (msg.channel.id != self.welcomeChannelID) and msg.channel.category != guild.categories[10]:
            timeInstant = datetime.now() + timedelta(seconds=60)

            def checkCallBack(m):
                return True

            await msg.channel.purge(before=timeInstant,
                                    check=checkCallBack)

            return

        #################################
        # Reset Welcome Channel Command #
        #################################
        if msg.content.startswith(self.BOTPREFIX + ' ResetWelcomeChannel') and isUserAdmin(
                msg.author.roles) and (msg.channel.id == self.welcomeChannelID):
            timeInstant = datetime.now() + timedelta(seconds=60)

            # Welcome/Rules Channel Setup with Custom message
            await msg.channel.purge(before=timeInstant)

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

            await msg.channel.send(embed=newWelcomeEmbed)
            m2 = await msg.channel.send(embed=newYOSEmbed)
            m3 = await msg.channel.send(embed=newStreamEmbed)

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

            return

        ################
        # Help Command #
        ################
        if msg.content.upper().startswith(self.BOTPREFIX + ' HELP'):
            helpDescrip = ''
            yearCategories = [
                guild.categories[3], guild.categories[4], guild.categories[5], guild.categories[6]]

            if msg.content.upper().startswith(self.BOTPREFIX + ' HELP '):
                cmdContent = msg.content.upper().split(
                    self.BOTPREFIX + ' HELP ')[1]
                cmdContent = cmdContent.lower()

                if msg.channel.id == self.adminCtrlChannelID:
                    if cmdContent == 'addcourse':
                        helpDescrip = helpmsg.addCourseLong
                    elif cmdContent == 'deletecourse':
                        helpDescrip = helpmsg.deleteCourseLong
                    elif cmdContent == 'archivecourse':
                        helpDescrip = helpmsg.archiveCourseLong
                    elif cmdContent == 'shutdown':
                        helpDescrip = helpmsg.shutdownLong
                    elif cmdContent == 'clearchannel':
                        helpDescrip = helpmsg.clearChannelLong
                    else:
                        helpDescrip = helpmsg.wrongHelp

                elif msg.channel.id == self.courseManagerChannelID:
                    if cmdContent == 'addcourse':
                        helpDescrip = helpmsg.addCourseLong
                    elif cmdContent == 'deletecourse':
                        helpDescrip = helpmsg.deleteCourseLong
                    elif cmdContent == 'archivecourse':
                        helpDescrip = helpmsg.deleteCourseLong
                    else:
                        helpDescrip = helpmsg.wrongHelp

                elif msg.channel.category == guild.categories[2]:
                    # upcoming commands
                    helpDescrip = helpmsg.generalHelp + '\n\n' + \
                        'Request courses and other features coming soon!'

                elif msg.channel.category in yearCategories:
                    # upcoming commands
                    helpDescrip = helpmsg.generalHelp + '\n\n' + \
                        'Request courses and other features coming soon!'

                elif msg.channel.category == guild.categories[9]:
                    if cmdContent == 'addproject':
                        helpDescrip = helpmsg.addProjectLong
                    elif cmdContent == 'deleteproject':
                        helpDescrip = helpmsg.deleteProjectLong
                    elif cmdContent == 'archiveproject':
                        helpDescrip = helpmsg.archiveProjectLong
                    else:
                        helpDescrip = helpmsg.wrongHelp

                elif msg.channel.category == guild.categories[10]:
                    if cmdContent == 'play':
                        helpDescrip = helpmsg.musicPlayLong
                    elif cmdContent == 'deleteproject':
                        helpDescrip = helpmsg.clearMusicLong
                    else:
                        helpDescrip = helpmsg.wrongHelp

                else:
                    helpDescrip == helpmsg.noHelp

            else:
                if msg.channel.id == self.adminCtrlChannelID:
                    helpDescrip = helpmsg.generalHelp
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.shutdownShort
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.clearChannelShort
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.addCourseShort
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.deleteCourseShort
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.archiveCourseShort

                elif msg.channel.id == self.courseManagerChannelID:
                    helpDescrip = helpmsg.generalHelp
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.addCourseShort
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.deleteCourseShort
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.archiveCourseShort

                elif msg.channel.category == guild.categories[2]:
                    helpDescrip = helpmsg.generalHelp + '\n\n' + \
                        'Request courses and other features coming soon!'

                elif msg.channel.category in yearCategories:
                    helpDescrip = helpmsg.generalHelp + '\n\n' + \
                        'Request courses and other features coming soon!'

                elif msg.channel.category == guild.categories[9]:
                    helpDescrip = helpmsg.generalHelp
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.addProjectShort
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.deleteProjectShort
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.archiveProjectShort

                elif msg.channel.category == guild.categories[10]:
                    helpDescrip = helpmsg.generalHelp
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.musicPlayShort
                    helpDescrip = helpDescrip + '\n\n' + helpmsg.clearMusicShort
                else:
                    helpDescrip = helpmsg.noHelp

            helpEmbed = discord.Embed(description=helpDescrip)
            helpEmbed.set_author(name="EEE Bot - Help Menu",
                                 icon_url=self.user.avatar_url)
            await msg.channel.send(embed=helpEmbed)

            return

        ##########################
        # New Suggestion Message #
        ##########################
        if msg.channel.category == guild.categories[11]:
            textchan = guild.get_channel(self.adminCtrlChannelID)

            newSuggestion = discord.Embed(
                description=msg.content + '\n\nMember: ' + msg.author.name, color=self.BOTCOLOR)

            if msg.channel.name == 'server-improvement':
                newSuggestion.set_author(name="Server Improvement Suggestion",
                                         icon_url=self.user.avatar_url)
            else:
                newSuggestion.set_author(name="Bug Report",
                                         icon_url=self.user.avatar_url)

            await textchan.send(embed=newSuggestion)

            return

        ###################
        # Invalid Command #
        ###################
        if msg.content.startswith('!EEE') or msg.content.startswith('!EE') or msg.content.startswith('!E') or msg.content.startswith('!'):
            await msg.channel.send(embed=discord.Embed(description=otherMsg.incorrectCommand))
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
                        description=messages.manageProject, color=self.BOTCOLOR)
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
            # get welcome channel and message that was reacted on
            m = await guild.get_channel(self.welcomeChannelID).fetch_message(payload.message_id)
            actionMember = await guild.fetch_member(payload.user_id)

            # remove unwanted reactions from message
            if (not str(payload.emoji) in self.emojis.values()) or (payload.message_id != self.streamMessageID and payload.message_id != self.yearOfStudyMessageID):
                await m.remove_reaction(payload.emoji, payload.member)
                return

            diagnosticsChan = guild.get_channel(self.diagnosticsChannelID)
            memberInfoEmbed = discord.Embed(description='Name: ' + actionMember.display_name + '\n\n Reaction Added: ' +
                                            str(payload.emoji) + '\n\n Time Reacted: ' + datetime.now().strftime("%d/%m/%Y @ %H:%M:%S"))

            # if the user reacting does not have a temp role dict
            # create an empty one for them
            if not payload.user_id in self.tempRoleConfig:
                self.tempRoleConfig[payload.user_id] = {
                    'years': [],
                    'stream': None,
                    'elective': False
                }

            # Append years of study to 'years': []
            if payload.message_id == self.yearOfStudyMessageID:
                memberInfoEmbed.set_author(
                    name=actionMember.name + ' - Year Reaction Add', icon_url=actionMember.avatar_url)
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

            # Set 'stream': '' according to reacted stream emoji
            if payload.message_id == self.streamMessageID:
                memberInfoEmbed.set_author(
                    name=actionMember.name + ' - Stream Reaction Add', icon_url=actionMember.avatar_url)

                oldStream = self.tempRoleConfig[payload.user_id]['stream']

                # Remove stream reaction if a new one is selected
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

                # check if user has any reaction selected on the stream msg
                hasUserReacted = False

                for react in m.reactions:
                    users = await react.users().flatten()
                    for user in users:
                        if user.id == payload.user_id:
                            hasUserReacted = True

                # if they have not reacted set the stream value to None
                # otherwise set the stream to the reaction emoji string
                if not hasUserReacted:
                    self.tempRoleConfig[payload.user_id]['stream'] = None
                else:
                    self.tempRoleConfig[payload.user_id]['stream'] = str(
                        payload.emoji)

            # finalise variables for addRoles function
            stream = self.tempRoleConfig[payload.user_id]['stream']
            years = self.tempRoleConfig[payload.user_id]['years']
            elective = self.tempRoleConfig[payload.user_id]['elective']

            # if the stream and years are both non Null values then assign the new roles
            if (stream != None and years != []) or elective:
                self.addRoles(payload.user_id, stream, years, elective)
                await payload.member.edit(roles=self.userRoleManagement[payload.user_id])
            else:
                await payload.member.edit(roles=[self.serverRoles['@everyone']])

            await diagnosticsChan.send(embed=memberInfoEmbed)

            return

    #########################
    # Reaction Remove Event #
    #########################

    async def on_raw_reaction_remove(self, payload):
        guild = self.guilds[0]
        actionMember = await guild.fetch_member(payload.user_id)

        # ensure that reaction removes by the bot are caught first and
        # method is escaped as this can cause issues with permissions
        # and incorrect users being assigned their roles
        if payload.user_id == self.user.id:
            return

        diagnosticsChan = guild.get_channel(self.diagnosticsChannelID)
        memberInfoEmbed = discord.Embed(description='Name: ' + actionMember.display_name + '\n\n Reaction Removed: ' +
                                        str(payload.emoji) + '\n\n Time Reacted: ' + datetime.now().strftime("%d/%m/%Y @ %H:%M:%S"))

        #########################
        # Role Reaction Manager #
        #########################
        if payload.channel_id == self.welcomeChannelID:
            # Remove year of study based on reaction emoji deselection
            if payload.message_id == self.yearOfStudyMessageID:
                memberInfoEmbed.set_author(
                    name=actionMember.name + ' - Year Reaction Remove', icon_url=actionMember.avatar_url)
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

            # remove stream if reaction deselected
            if payload.message_id == self.streamMessageID:
                memberInfoEmbed.set_author(
                    name=actionMember.name + ' - Stream Reaction Remove', icon_url=actionMember.avatar_url)
                self.tempRoleConfig[payload.user_id]['stream'] = None

            # finalise variables for addRoles function
            stream = self.tempRoleConfig[payload.user_id]['stream']
            years = self.tempRoleConfig[payload.user_id]['years']

            self.addRoles(payload.user_id, stream, years,
                          self.tempRoleConfig[payload.user_id]['elective'])

            # if the stream and years are not empty assign the roles otherwise remove all roles
            if stream != None and years != []:
                await actionMember.edit(roles=self.userRoleManagement[payload.user_id])
            else:
                await actionMember.edit(roles=[self.serverRoles['@everyone']])

            await diagnosticsChan.send(embed=memberInfoEmbed)

            return

    #################
    # On Join Event #
    #################
    async def on_member_join(self, member):
        guild = self.guilds[0]
        diagnosticsChan = guild.get_channel(self.diagnosticsChannelID)
        memberInfoEmbed = discord.Embed(description='Name: ' + member.display_name + '\n\n Member Since: ' +
                                        member.joined_at.strftime("%d/%m/%Y @ %H:%M:%S") + '\n\n Discord User Since: ' + member.created_at.strftime("%d/%m/%Y @ %H:%M:%S"))
        memberInfoEmbed.set_author(
            name=member.name + ' joined!', icon_url=member.avatar_url)
        await diagnosticsChan.send(embed=memberInfoEmbed)

    #################
    # On Leave Event #
    #################
    async def on_member_remove(self, member):
        guild = self.guilds[0]
        diagnosticsChan = guild.get_channel(self.diagnosticsChannelID)
        memberInfoEmbed = discord.Embed(
            description='Name: ' + member.display_name)
        memberInfoEmbed.set_author(
            name=member.name + ' left!', icon_url=member.avatar_url)
        await diagnosticsChan.send(embed=memberInfoEmbed)


##############
# Client run #
##############
client = UniDiscordBot(intents=intents)
client.run(os.getenv('TOKEN'))
