# Base slash command
START_WITH_EMOJI_SLASH = r'(\W |\/)?'

# Hours and minutes
HOURS_COMMAND = r'((H|h)ora(s)?)'
HOURS_OFFLINE_ADD = r'^(\+\s?\d+\s?((:|(H|h)(ora|r)?(s)?)\s?([0-5]?[0-9])\s?(((M|m)(in(uto(s)?)?)?)|((H|h)(ora|r)?(s)?))?|((H|h)(ora|r)?(s)?)))$'
HOURS_OFFLINE_REMOVE = r'^(\-\s?\d+\s?((:|(H|h)(ora|r)?(s)?)\s?([0-5]?[0-9])\s?(((M|m)(in(uto(s)?)?)?)|((H|h)(ora|r)?(s)?))?|((H|h)(ora|r)?(s)?)))$'
HOURS_OFFLINE_ADD_MINUTES = r'\+\s?[0-5]?[0-9]\s?((M|m)(in)?(uto)?(s)?)'
HOURS_OFFLINE_REMOVE_MINUTES = r'\-\s?[0-5]?[0-9]\s?((M|m)(in)?(uto)?(s)?)'

# Videos
VIDEO_COMMAND = r'((V|v)(í|i)deo(s)?)'
VIDEO_OFFLINE_ADD = r'^(\+\s?\d+\s?((V|v)(i|í)?(d)?(eo)?(s)?))$'
VIDEO_OFFLINE_REMOVE = r'^(\-\s?\d+\s?((V|v)(i|í)?(d)?(eo)?(s)?))$'

# Publications
PUBS_COMMAND = r'((P|p)ublica(c|\S)((a|\S)|(o|\S))(\w+)?)'
PUBS_OFFLINE_ADD = r'^(\+\s?\d+\s?((P|p)(ub(lica(ç|c)(.+))?(s)?)?))$'
PUBS_OFFLINE_REMOVE = r'^(\-\s?\d+\s?((P|p)(ub(lica(ç|c)(.+))?(s)?)?))$'

# Returns
RETURNS_COMMAND = r'((R|r)evisita(s)?)'
RETURNS_OFFLINE_ADD = r'^(\+\s?\d+\s?((R|r)(ev(s)?)?(isit(.*)?)?))$'
RETURNS_OFFLINE_REMOVE = r'^(\-\s?\d+\s?((R|r)(ev(s)?)?(isit(.*)?)?))$'

# Studies
STUDIES_COMMAND = r'((E|e)stud(\w+))'
STUDIES_OFFLINE_ADD = r'^(\+\s?\d+\s?((E|e)(st(ud\w+)?)?))$'
STUDIES_OFFLINE_REMOVE = r'^(\-\s?\d+\s?((E|e)(st(ud\w+)?)?))$'

# Others Commands Foo
CRON_COMMAND = r'((C|c)ron((o|\S)metr(\w+))?)'
REPORT_COMMAND = r'((R|r)elat(o|\S)ri(o|os))'
HELP_COMMAND = r'(A|a)jud(a|e|o)'
NOT_FOUND_404 = r'.+'



