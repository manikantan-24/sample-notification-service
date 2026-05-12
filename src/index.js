const express = require('express')
const nodemailer = require('nodemailer')
const Queue = require('bull')
const _ = require('lodash')
const winston = require('winston')

const app = express()
const emailQueue = new Queue('email')

const logger = winston.createLogger({
  transports: [new winston.transports.Console()],
})

app.use(express.json())

app.post('/notify/email', async (req, res) => {
  const { to, subject, body } = req.body
  await emailQueue.add({ to, subject, body })
  logger.info('queued email', { to })
  res.json({ queued: true })
})

app.post('/notify/sms', async (req, res) => {
  res.json({ queued: true, channel: 'sms' })
})

app.listen(4000, () => logger.info('notification service on :4000'))
