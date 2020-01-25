import threading


class BookingThread (threading.Thread):

    def __init__(self, session, offset, rooms, country,dest_id,DayIni, DayFim, process_hotels):
        threading.Thread.__init__(self)
        self.session = session
        self.offset  = offset
        self.rooms   = rooms
        self.country = country
        self.dest_id = dest_id
        self.DayIni = DayIni
        self.DayFim = DayFim
        self.process_hotels = process_hotels

    def run(self):
        self.process_hotels(self.session, self.offset, self.rooms, self.country,self.dest_id,self.DayIni,self.DayFim)
